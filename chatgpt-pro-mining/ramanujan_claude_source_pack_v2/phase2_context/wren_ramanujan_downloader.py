#!/usr/bin/env python3
"""
Bulk downloader for Trinity/Wren Ramanujan manuscript page images.

Targets:
  - Trinity College Cambridge Add. MS a/94.1-18 (Ramanujan papers)
  - optional Add. MS a/396 (letters to E. H. Neville)

The script is intentionally conservative:
  * It starts from public viewer URLs and/or IIIF manifests.
  * It stores the manifest JSON verbatim.
  * It derives IIIF Image API URLs from manifest services.
  * It writes page-level source URLs, status, size, and SHA-256 checksums.
  * It skips already downloaded files unless --refresh is supplied.

Usage:
  python scripts/wren_ramanujan_downloader.py \
      --targets ramanujan_wren_targets.csv \
      --out ./ramanujan_wren_download \
      --delay 0.75

Dependencies:
  pip install requests tqdm

Notes:
  Trinity's Wren/AtoM pages can expose IIIF manifests in more than one URL pattern.
  This script tries both direct candidate manifest URLs and viewer HTML scraping for
  manifestUri parameters. It supports IIIF Presentation API v2 and v3 enough for
  page-image extraction.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import unquote, urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
try:
    from urllib3.util.retry import Retry
except Exception:  # pragma: no cover
    Retry = None


DEFAULT_USER_AGENT = (
    "RamanujanResearchDownloader/0.1 "
    "(+research use; please contact requester if traffic is problematic)"
)

IMAGE_EXT_BY_TYPE = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/tiff": ".tif",
    "image/webp": ".webp",
}


@dataclass
class PageRecord:
    reference_code: str
    manifest_url: str
    canvas_index: int
    canvas_label: str
    canvas_id: str
    image_url: str
    local_path: str
    sha256: str
    bytes: int
    content_type: str
    status: str
    note: str = ""


def session_with_retries(user_agent: str, retries: int = 4) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": user_agent,
        "Accept": "application/json,text/html,image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    })
    if Retry is not None:
        retry = Retry(
            total=retries,
            connect=retries,
            read=retries,
            status=retries,
            backoff_factor=0.75,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "HEAD"),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=8, pool_maxsize=8)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
    return s


def safe_name(ref: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", ref.strip().replace("/", "."))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_manifest_candidates(reference_code: str, viewer_url: str, candidate_field: str = "") -> List[str]:
    """Generate plausible IIIF manifest URLs for Wren modern-manuscript viewer items."""
    out: List[str] = []
    for part in re.split(r"\s*\|\s*", candidate_field or ""):
        part = part.strip()
        if part:
            out.append(part)

    # Extract n= from viewer URL when possible.
    n = ""
    m = re.search(r"[?&]n=([^&#]+)", viewer_url)
    if m:
        n = unquote(m.group(1))
    if not n:
        # Add. MS a/94/15 -> Add.Ms.a.94.15-ish
        n = reference_code.replace("MS", "Ms").replace(" ", ".").replace("/", ".")
        n = re.sub(r"\.+", ".", n)

    variants = []
    for base in {n, n.lower(), n.replace("MS", "Ms"), n.replace("MS", "Ms").lower()}:
        base = base.strip()
        if not base:
            continue
        variants.append(base)
        pieces = base.split(".")
        # Some Wren modern manifests use an underscore before subitem number, e.g. Add.Ms.a.614_12.
        if len(pieces) >= 5:
            variants.append(".".join(pieces[:-1]) + "_" + pieces[-1])
    for v in variants:
        out.extend([
            f"https://mss-cat.trin.cam.ac.uk/manuscripts/{v}.json",
            f"https://mss-cat.trin.cam.ac.uk/manuscripts/{v}/manifest.json",
        ])

    # Deduplicate preserving order.
    seen = set()
    deduped = []
    for u in out:
        if u not in seen:
            seen.add(u)
            deduped.append(u)
    return deduped


def extract_manifest_urls_from_html(viewer_html: str, base_url: str) -> List[str]:
    """Find manifestUri or .json URLs embedded in Wren/UniversalViewer pages."""
    text = html.unescape(viewer_html)
    urls: List[str] = []

    patterns = [
        r"manifestUri=([^&\"'<>\s]+)",
        r"manifest_uri=([^&\"'<>\s]+)",
        r"manifest=([^&\"'<>\s]+\.json[^&\"'<>\s]*)",
        r"[\"']manifestUri[\"']\s*[:=]\s*[\"']([^\"']+)[\"']",
        r"[\"']manifest[\"']\s*[:=]\s*[\"']([^\"']+\.json[^\"']*)[\"']",
        r"(https?://[^\"'<>\s]+\.json[^\"'<>\s]*)",
        r"([./A-Za-z0-9_%:-]+\.json(?:\?[^\"'<>\s]*)?)",
    ]
    for pat in patterns:
        for match in re.findall(pat, text):
            if isinstance(match, tuple):
                match = match[0]
            u = unquote(match).strip()
            if not u or u.startswith("data:"):
                continue
            if not u.startswith("http"):
                u = urljoin(base_url, u)
            # Avoid UV config/localization JSON unless we have no other option.
            if any(skip in u.lower() for skip in ("locale", "config", "package", "manifesto.js")):
                continue
            urls.append(u)

    # Deduplicate preserving order.
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def load_targets(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_json(session: requests.Session, url: str, timeout: int = 60) -> Tuple[Optional[Dict[str, Any]], str]:
    try:
        r = session.get(url, timeout=timeout)
        ct = r.headers.get("content-type", "")
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}; content-type={ct}"
        # Some servers label IIIF JSON as text/plain or application/ld+json.
        try:
            return r.json(), f"OK; content-type={ct}; bytes={len(r.content)}"
        except Exception as e:
            preview = r.text[:160].replace("\n", " ")
            return None, f"JSON parse failed: {e}; content-type={ct}; preview={preview!r}"
    except Exception as e:
        return None, f"request failed: {type(e).__name__}: {e}"


def discover_manifest(session: requests.Session, target: Dict[str, str], log) -> Tuple[Optional[Dict[str, Any]], Optional[str], List[str]]:
    ref = target.get("reference_code", "")
    viewer = target.get("viewer_url", "")
    candidate_field = target.get("candidate_manifest_urls", "")
    tried: List[str] = []

    # First try explicit/candidate manifest URLs.
    candidates = normalize_manifest_candidates(ref, viewer, candidate_field)
    for url in candidates:
        tried.append(url)
        manifest, msg = get_json(session, url)
        log.write(f"[{ref}] manifest candidate {url} -> {msg}\n")
        if manifest and looks_like_iiif_manifest(manifest):
            return manifest, url, tried

    # Then scrape the viewer HTML for a manifestUri or embedded app URL.
    if viewer:
        try:
            r = session.get(viewer, timeout=60)
            log.write(f"[{ref}] viewer {viewer} -> HTTP {r.status_code}; content-type={r.headers.get('content-type','')} bytes={len(r.content)}\n")
            if r.status_code == 200:
                html_urls = extract_manifest_urls_from_html(r.text, viewer)
                for url in html_urls:
                    if url in tried:
                        continue
                    tried.append(url)
                    manifest, msg = get_json(session, url)
                    log.write(f"[{ref}] html-discovered manifest {url} -> {msg}\n")
                    if manifest and looks_like_iiif_manifest(manifest):
                        return manifest, url, tried
        except Exception as e:
            log.write(f"[{ref}] viewer scrape failed: {type(e).__name__}: {e}\n")

    return None, None, tried


def looks_like_iiif_manifest(obj: Dict[str, Any]) -> bool:
    if not isinstance(obj, dict):
        return False
    if "sequences" in obj or "items" in obj:
        return True
    t = obj.get("@type") or obj.get("type")
    return isinstance(t, str) and "Manifest" in t


def as_list(x: Any) -> List[Any]:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def label_to_str(label: Any) -> str:
    if label is None:
        return ""
    if isinstance(label, str):
        return label
    if isinstance(label, dict):
        # IIIF v3 language map, or v2 @value.
        if "@value" in label:
            return str(label["@value"])
        vals = []
        for v in label.values():
            if isinstance(v, list):
                vals.extend(str(i) for i in v)
            else:
                vals.append(str(v))
        return "; ".join(vals)
    return str(label)


def service_id(service: Any) -> Optional[str]:
    for svc in as_list(service):
        if isinstance(svc, dict):
            sid = svc.get("@id") or svc.get("id")
            if sid:
                return str(sid).rstrip("/")
    return None


def image_candidates_from_body(body: Dict[str, Any]) -> List[str]:
    urls: List[str] = []
    if not isinstance(body, dict):
        return urls

    # Direct image URL.
    direct = body.get("@id") or body.get("id")
    if isinstance(direct, str) and re.search(r"\.(jpe?g|png|tif|tiff|webp)(\?|$)", direct, re.I):
        urls.append(direct)

    sid = service_id(body.get("service"))
    if sid:
        # IIIF Image API common size forms. Try full first for archival quality.
        urls.extend([
            f"{sid}/full/full/0/default.jpg",     # IIIF v2 common
            f"{sid}/full/max/0/default.jpg",      # IIIF v3 common
            f"{sid}/full/!5000,5000/0/default.jpg",
            f"{sid}/full/!3000,3000/0/default.jpg",
            f"{sid}/full/1000,/0/default.jpg",
        ])
    elif isinstance(direct, str):
        urls.append(direct)
    return urls


def iter_manifest_pages(manifest: Dict[str, Any]) -> Iterable[Tuple[int, str, str, List[str]]]:
    """Yield (index, canvas_label, canvas_id, candidate_image_urls)."""
    # IIIF Presentation API v2
    sequences = manifest.get("sequences")
    if sequences:
        canvases = sequences[0].get("canvases", []) if isinstance(sequences[0], dict) else []
        for idx, canvas in enumerate(canvases, start=1):
            label = label_to_str(canvas.get("label")) or f"page {idx}"
            cid = str(canvas.get("@id") or canvas.get("id") or "")
            urls: List[str] = []
            for ann in as_list(canvas.get("images")):
                if not isinstance(ann, dict):
                    continue
                resource = ann.get("resource") or ann.get("body")
                if isinstance(resource, dict):
                    urls.extend(image_candidates_from_body(resource))
            yield idx, label, cid, dedupe(urls)
        return

    # IIIF Presentation API v3
    items = manifest.get("items", [])
    for idx, canvas in enumerate(items, start=1):
        if not isinstance(canvas, dict):
            continue
        label = label_to_str(canvas.get("label")) or f"page {idx}"
        cid = str(canvas.get("id") or canvas.get("@id") or "")
        urls: List[str] = []
        for anno_page in as_list(canvas.get("items")):
            if not isinstance(anno_page, dict):
                continue
            for ann in as_list(anno_page.get("items")):
                if not isinstance(ann, dict):
                    continue
                body = ann.get("body") or ann.get("resource")
                for b in as_list(body):
                    if isinstance(b, dict):
                        urls.extend(image_candidates_from_body(b))
        yield idx, label, cid, dedupe(urls)


def dedupe(items: Iterable[str]) -> List[str]:
    seen = set(); out = []
    for item in items:
        if item and item not in seen:
            seen.add(item); out.append(item)
    return out


def download_image(
    session: requests.Session,
    candidate_urls: List[str],
    out_base: Path,
    refresh: bool,
    dry_run: bool,
    timeout: int = 120,
) -> Tuple[Optional[Path], str, str, int, str, str]:
    """Try candidate image URLs. Returns path, chosen_url, sha256, bytes, content_type, status_note."""
    if not candidate_urls:
        return None, "", "", 0, "", "no image candidate URLs in canvas"

    # If already exists, use it and keep current source unknown unless source CSV exists.
    existing = list(out_base.parent.glob(out_base.name + ".*"))
    if existing and not refresh:
        p = existing[0]
        return p, candidate_urls[0], sha256_file(p), p.stat().st_size, "", "already existed; skipped"

    if dry_run:
        return None, candidate_urls[0], "", 0, "", "dry-run; not downloaded"

    last_note = ""
    for url in candidate_urls:
        try:
            r = session.get(url, timeout=timeout)
            ct = r.headers.get("content-type", "").split(";")[0].strip().lower()
            if r.status_code != 200:
                last_note = f"{url}: HTTP {r.status_code}; content-type={ct}"
                continue
            if not (ct.startswith("image/") or r.content[:4] in (b"\xff\xd8\xff\xe0", b"\xff\xd8\xff\xe1") or r.content[:8].startswith(b"\x89PNG")):
                preview = r.content[:80].decode("utf-8", errors="replace").replace("\n", " ")
                last_note = f"{url}: not image; content-type={ct}; preview={preview!r}"
                continue
            ext = IMAGE_EXT_BY_TYPE.get(ct) or guess_ext_from_url(url) or ".jpg"
            path = out_base.with_suffix(ext)
            path.write_bytes(r.content)
            return path, url, sha256_bytes(r.content), len(r.content), ct, "downloaded"
        except Exception as e:
            last_note = f"{url}: {type(e).__name__}: {e}"
    return None, candidate_urls[0], "", 0, "", f"all image candidates failed; last={last_note}"


def guess_ext_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ""


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", type=Path, required=True, help="CSV target list")
    ap.add_argument("--out", type=Path, required=True, help="Output directory")
    ap.add_argument("--delay", type=float, default=0.75, help="Delay in seconds between page downloads")
    ap.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    ap.add_argument("--refresh", action="store_true", help="Re-download existing files")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-pages-per-target", type=int, default=0, help="0 means no limit")
    ap.add_argument("--only", default="", help="Comma-separated reference codes to download")
    args = ap.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "manifests").mkdir(exist_ok=True)
    (args.out / "wren_pages").mkdir(exist_ok=True)
    (args.out / "logs").mkdir(exist_ok=True)

    targets = load_targets(args.targets)
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    if only:
        targets = [t for t in targets if t.get("reference_code") in only]

    session = session_with_retries(args.user_agent)
    page_rows: List[Dict[str, Any]] = []
    failure_rows: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    with (args.out / "logs" / "download.log").open("a", encoding="utf-8") as log:
        log.write(f"\n=== run start {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        log.write(f"dry_run={args.dry_run} refresh={args.refresh} delay={args.delay}\n")
        for target in targets:
            ref = target.get("reference_code", "unknown")
            safe_ref = safe_name(ref)
            print(f"== {ref} ==", file=sys.stderr)
            target_dir = args.out / "wren_pages" / safe_ref
            target_dir.mkdir(parents=True, exist_ok=True)

            manifest, manifest_url, tried = discover_manifest(session, target, log)
            if not manifest or not manifest_url:
                failure_rows.append({
                    "reference_code": ref,
                    "stage": "manifest_discovery",
                    "detail": "No IIIF manifest found or fetchable",
                    "tried_urls": " | ".join(tried),
                })
                summary_rows.append({
                    "reference_code": ref,
                    "manifest_url": "",
                    "pages_seen": 0,
                    "pages_downloaded_or_present": 0,
                    "failures": 1,
                })
                continue

            manifest_path = args.out / "manifests" / f"{safe_ref}.manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

            pages_seen = 0
            pages_ok = 0
            failures = 0
            for idx, label, canvas_id, img_urls in iter_manifest_pages(manifest):
                if args.max_pages_per_target and idx > args.max_pages_per_target:
                    break
                pages_seen += 1
                out_base = target_dir / f"page_{idx:04d}"
                path, chosen_url, digest, nbytes, ct, note = download_image(
                    session, img_urls, out_base, args.refresh, args.dry_run
                )
                status = "ok" if path else "failed"
                if path:
                    pages_ok += 1
                else:
                    failures += 1
                    failure_rows.append({
                        "reference_code": ref,
                        "stage": f"image_download_page_{idx:04d}",
                        "detail": note,
                        "tried_urls": " | ".join(img_urls),
                    })
                rec = PageRecord(
                    reference_code=ref,
                    manifest_url=manifest_url,
                    canvas_index=idx,
                    canvas_label=label,
                    canvas_id=canvas_id,
                    image_url=chosen_url,
                    local_path=str(path or ""),
                    sha256=digest,
                    bytes=nbytes,
                    content_type=ct,
                    status=status,
                    note=note,
                )
                page_rows.append(asdict(rec))
                log.write(f"[{ref}] page {idx:04d}: {status}; {note}; {chosen_url}\n")
                time.sleep(max(args.delay, 0))

            summary_rows.append({
                "reference_code": ref,
                "manifest_url": manifest_url,
                "pages_seen": pages_seen,
                "pages_downloaded_or_present": pages_ok,
                "failures": failures,
            })

    write_csv(args.out / "page_image_manifest.csv", page_rows, list(PageRecord.__dataclass_fields__.keys()))
    write_csv(args.out / "failures.csv", failure_rows, ["reference_code", "stage", "detail", "tried_urls"])
    write_csv(args.out / "download_summary.csv", summary_rows, ["reference_code", "manifest_url", "pages_seen", "pages_downloaded_or_present", "failures"])

    print(f"Wrote: {args.out}")
    print(f"Pages ok/present: {sum(int(r['pages_downloaded_or_present']) for r in summary_rows)}")
    print(f"Failures: {sum(int(r['failures']) for r in summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

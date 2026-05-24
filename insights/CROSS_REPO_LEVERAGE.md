# Cross-repo leverage — does rkc/Ramanujan work help the other repos?

User asked whether the work in this repo is useful for the sibling projects
they're running:

- `/Users/jouni/Documents/aether-audio` — passivity-accounted differentiable
  physical audio graphs, Rust realtime, grey-box identification
- `/Users/jouni/Documents/aether-hardware-ebm` — mixed-signal local
  equilibrium/response primitives, EqProp (equilibrium propagation), Schur
  boundary reduction, crosspoint surrogates
- `/Users/jouni/Documents/arc-agi-ebm-agent` — ARC-AGI object-centric program
  induction + EBM-style proposal/ranking, SDM/JEPA-related experiments,
  verifier-first planning

**Honest read:** the Ramanujan-specific kernels (theta, mock-theta, Lambert,
Eisenstein, …) are unlikely to fire directly on any of these. **But the
[rkc/](../rkc/) *architecture* — registry + matcher + cost model + certificate
+ degeneracy detector — is a transferable pattern**, and there are 3-4 specific
narrow connections worth flagging beyond pattern-transfer.

This file captures the strategic mapping so it survives the conversation.
Concrete cross-repo action items are in [todo.md](../todo.md) §"Cross-repo".

---

## The transferable pattern

The thing that makes [rkc/](../rkc/) worth shipping isn't "theta transforms
are fast". It's the engineering discipline:

1. **Per-kernel matchers** — identify which family a structured computation
   belongs to.
2. **Per-route cost models** — for each family, score each evaluation
   strategy (direct / closed-form / approximation / dual representation).
3. **Per-route certificates** — emit a verifiable bound on truncation error
   / approximation quality for the chosen route.
4. **Per-family degeneracy detectors** — refuse routes that look
   mathematically legal but produce wrong answers in known regimes (e.g.
   Gauss sums q ≡ 2 mod 4 silent-zero hazard,
   [CANDIDATE_INSIGHTS §A4](CANDIDATE_INSIGHTS.md)).
5. **CLI + Python API surface** — make the routing decision observable to
   downstream tooling.

That pattern applies wherever there's: (i) a small vocabulary of structured
computations, (ii) multiple equivalent evaluation strategies with non-trivial
cost trade-offs, (iii) per-strategy failure modes that look like legal
computations but give wrong answers.

**All three sibling repos match (i)-(iii).**

---

## aether-audio — passivity-accounted physical audio graphs

What it actually does: differentiable physical audio (resonators, filters,
couplings) with **passivity** as the structural invariant. Energy/power
telemetry is a first-class proof artefact. Grey-box identification = fitting
parameters to physical structure on paired dry/wet recordings.

**Direct connections:**
- **The rkc pattern applies almost verbatim.** A `rkc_phs` registry would
  hold kernels for passive physical-audio primitives: resonators, all-pass
  filters, waveguides, FDN topologies. Each kernel has:
  - Matcher: identify the topology from the network's adjacency + parameter
    structure
  - Per-route cost: direct time-domain stepping vs frequency-domain
    convolution vs modal expansion
  - Certificate: passivity bound (energy in ≥ energy out + dissipation)
  - Degeneracy detector: combinations of parameters that produce silent
    passivity violation (e.g. cancellation that NaN's the energy balance)
- **Theta-function dual representations are directly relevant** for any
  high-Q resonator at low damping. The Gaussian theta is the Poisson
  summation of an impulse train; the recognizer's β\* = c·π crossover
  ([CANDIDATE_INSIGHTS §A6](CANDIDATE_INSIGHTS.md)) is exactly the crossover
  between time-domain and frequency-domain evaluation. **This is one
  concrete kernel that could move from rkc to rkc_phs unchanged.**
- **The silent-zero-hazard pattern transfers cleanly.** PHS proof bookkeeping
  needs to refuse certain transformations that violate passivity at
  parameter edges (negative dissipation, energy injection from
  discretisation). The rkc/certify CLI shape is what aether-audio's
  proof gates want.

**Narrow connection (speculative):**
- QR III's Schröder/Koenig fractional-iteration material gives explicit
  closed-form `F^n(x)` for one-parameter semigroups. Audio resonators are
  one-parameter semigroups (in time). For nonlinear resonators (e.g.
  Duffing, Van der Pol) the Schröder linearisation may give a closed-form
  evaluation that beats stepping for short windows. **Untested**;
  speculative match.

**Recommended cross-repo task:** scope a `rkc_phs` registry skeleton —
borrow the rkc/ architecture, plug in the first 3-5 PHS primitives, get
the certificate emission working for energy balance. Half-week effort.
See [todo.md](../todo.md) X1.

---

## aether-hardware-ebm — Schur boundary, EqProp, crosspoint surrogates

What it actually does: mixed-signal local equilibrium primitives behind
low-dimensional digital boundaries. **EqProp = a literal EBM training
method** (Scellier-Bengio). H4 evidence accounting is the proof-bookkeeping
discipline.

**Direct connections:**
- **EqProp training requires repeated Z(β) computations** — exactly the
  partition-function-like quantity rkc is designed to route. For EBMs with
  structured energy (lattice geometry, quadratic-form coupling, symmetry
  groups), the rkc/recognize → rkc/route path gives **per-batch certified
  evaluation** of the normaliser, skipping the MCMC inner loop entirely.
  This is potentially a huge win for EqProp training on structured
  energies — same direction as Pass A's quantified 10¹-10⁵× term-count
  reductions ([CANDIDATE_INSIGHTS §A1](CANDIDATE_INSIGHTS.md)).
- **The B1 closure result tells aether-hardware-ebm what KIND of EBMs
  *cannot* be losslessly mapped to analog primitives**: if the partition
  function has H¹(Γ, V_k) Eichler cocycle structure, no finite-K analog
  tile can replicate it ([CANDIDATE_INSIGHTS §B](CANDIDATE_INSIGHTS.md),
  Exp 22). This is a real architectural constraint for analog-EBM
  acceleration — it tells the hardware repo what its analog tiles need to
  NOT promise to do. Concrete: any "mock modular" generative-model class
  is fundamentally beyond the reach of the crosspoint primitive.
- **H4 evidence accounting ≈ rkc certificate emission**. The fail-closed
  pattern (H4 is the evidence-gate level) is structurally identical to
  rkc/certify's "do NOT use the dual" refusal. **The discipline transfers
  bidirectionally**: aether-hardware-ebm's H4 vocabulary could inform the
  rkc certificate schema; rkc's per-family degeneracy detectors could
  inform aether-hardware's per-primitive failure-mode contracts.

**Narrow connection:**
- The Berndt-Dixit 2009 αβ=1 transformation (H10) involves Γ'/Γ + Riemann
  Ξ. Spectral theory of self-adjoint operators uses similar machinery.
  Mixed-signal crosspoint conductance arrays are physical instantiations
  of self-adjoint matrices. **Untested** whether the αβ=1 transformation
  has a direct analog-implementation shortcut, but worth a 1-day scope.

**Recommended cross-repo task:** import the rkc/certify pattern as the
template for H4 boundary-evidence claim contracts. The rkc CLI shape
(recognize/compare/certify) maps cleanly onto the existing hardware\_\*
scripts. Half-week effort. See [todo.md](../todo.md) X2.

---

## arc-agi-ebm-agent — object-centric program induction + EBM ranking

What it actually does: interactive analysis-by-synthesis for ARC-AGI. Build
object/event state, infer executable transition/goal hypotheses, choose
probes by counterfactual disagreement, **rank with energy/surprise**, adapt
sparse memory over rule signatures. Verifier-first planning.

**Direct connections:**
- **The W5/T3 operator-composition search engine maps DIRECTLY onto
  ARC-AGI's program-induction loop.** Generate candidates by composing
  operators from a small DSL, numerically verify, rank by energy. This is
  structurally identical to what an ARC solver does. The Ramanujan
  7-operator basis from Hunt 5 is a SMALL discrete vocabulary for a math
  domain — analogous to ARC's DSL. **The operator-composition search
  prototype proposed for rkc (W5) is, abstractly, the same algorithm as
  ARC's program-rank stage.** Building one validates the other.
- **The KernelFamily enum (small finite vocabulary, content-addressable) is
  structurally a sparse distributed memory (SDM).** Each family has a
  fingerprint (matcher), an addressable name (kernel_id), and a content
  (routing strategy + cost + certificate). ARC's SDM/intent layer wants the
  same shape: rule signatures addressable by their fingerprint, with a
  routing strategy attached.
- **Verifier-first planning ≈ certify-before-route**. The discipline is
  identical: don't commit to a transformation until you've certified it's
  safe under the current parameters. The rkc/certify CLI is a concrete
  template for the verifier-first stage.

**Narrow connections:**
- The Hunt 5 finding that the 6-predicted operators were wrong but a
  7-operator revised basis covers 91% is methodologically relevant to ARC:
  **the initial DSL is almost always wrong; the empirical correction is
  the work**. The discipline of "predict basis → tag → revise basis →
  re-test on held-out chapter" is exactly what an ARC agent's
  rule-discovery loop should do.
- The "small toolkit per problem-domain" framing
  ([BIG_IDEAS_REVIEW §2a](BIG_IDEAS_REVIEW.md)) — Ramanujan deployed
  different operator subsets per problem class — is conceptually the same
  as ARC's "different rule families per task type". **The toolkit-split
  hypothesis is testable on ARC's task taxonomy** if you have per-task
  rule-fingerprint tags.

**Recommended cross-repo task:** make T3 (operator-composition search
prototype) a *shared* effort. Build the search engine on the Ramanujan
operator basis (small, well-defined) as the validation case; refactor the
engine so the operator basis is pluggable; plug in ARC's DSL as the second
test case. The reusable artefact is `rkc.search` or a new
`compositional_search` package both repos depend on. ~1-2 weeks; see
[todo.md](../todo.md) X3.

---

## Connection-strength summary

| Direction | Strength | Concrete next step |
|---|---|---|
| rkc → aether-audio | **Strong (pattern + theta-direct kernels)** | X1: scope `rkc_phs` registry, half-week |
| rkc → aether-hardware-ebm | **Strong (pattern + B1 constraint + EqProp Z(β))** | X2: import certify pattern as H4 template, half-week |
| rkc → arc-agi-ebm-agent | **Strong (W5 search ≡ ARC program induction)** | X3: build T3 search engine as shared artefact, 1-2 weeks |
| aether-audio → rkc | weak | (PHS energy-balance vocabulary informs certificate schema) |
| aether-hardware-ebm → rkc | medium | H4 evidence accounting could inform rkc certificate granularity |
| arc-agi-ebm-agent → rkc | medium | ARC's rule-signature taxonomy could inform `KernelFamily` enum structure |

---

## What is NOT shared (calibration)

- Ramanujan's specific kernels (theta, mock-theta f3/f5/f7, Lambert,
  Eisenstein, …) are unlikely to fire directly on any sibling repo's
  computations. The kernels in `rkc/registry.py` stay specific to the
  Ramanujan corpus.
- The historical findings (W8 pre-Julia, H1c Diophantine priority,
  canonical-narrowing meta-finding) are number-theory / math-history; no
  cross-repo leverage.
- The cohomological-irreducibility conjecture (B1 closed) is a *negative*
  result for the modular case; it does NOT directly help the sibling repos
  beyond the architectural constraint flagged above.
- The Hunt 5 / Hunt 5b operator-tagging methodology is specific to reading
  primary mathematical text; doesn't transfer to ARC or audio.

The honest summary: **architectural patterns transfer; specific results
do not**. The headline transferable artefact is rkc itself (CLI + API +
registry pattern + degeneracy-detector discipline).

---

## See also

- [BIG_IDEAS_REVIEW.md](BIG_IDEAS_REVIEW.md) — full ranking of run-internal
  big ideas; X1-X3 below are cross-repo extensions of the T1-T4 tool-side
  stack.
- [rkc/MILESTONES.md](../rkc/MILESTONES.md) — the v0.1 release gates that
  X1-X3 would build on top of.
- [todo.md](../todo.md) §"Cross-repo" — concrete X1/X2/X3 action items.

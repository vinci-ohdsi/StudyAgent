# Current Sprint Plan

## Objective

Make the completed `/ohdsi` Atlas concept-set and cohort-assistance work
reproducible and meeting-ready in `sandbox/AtlasWebAPISandbox`, then strengthen
terminology retrieval and extend cohort composition only through explicit,
review-gated templates.

The immediate priority is a credible Thursday demonstration. It must run from
recorded source checkpoints and local configuration; it must not imply that a
portable production container stack or a redistributable Athena vocabulary
fixture already exists.

## 1. Meeting-ready `AtlasWebAPISandbox` demo — first priority

Create a runnable `demos/study-agent-demo` profile using the established sprint
checkpoint tags as its exact source boundary.

### Deliverables

- Pin the demo manifest to the StudyAgent, Atlas3, WebAPI3, and documentation
  tags from the completed sprint.
- Provide a local configuration template for WebAPI feature flags, the ACP/MCP
  endpoint, database connection, and Atlas origin. Do not commit secrets.
- Provide an ordered startup and verification runbook (or a narrow helper
  script) that checks migrations, permissions, `/ohdsi` availability, and
  service connectivity.
- Document a meeting walkthrough with three reliable stories:
  1. `/ohdsi` concept-set creation and explicit Selected/Included review.
  2. Phenotype recommendation or library candidate to an unsaved Circe draft.
  3. Esketamine exposure plus MDD supporting evidence to a reviewed
     multi-component plan and unsaved cohort draft.
- Include a browser/network verification that Atlas calls WebAPI only; the
  browser must not call ACP or MCP directly.
- Add a lightweight smoke check for the deployed local profile where practical.

### Boundary

This is a source-built/local integration profile for the meeting. Digest-pinned
containers, a portable compose stack, and a licensed vocabulary-fixture build
remain follow-up hardening work.

## 2. Vocabulary retrieval correctness and review scale

Address the gap demonstrated by ingredient-level ADHD requests before adding
more cohort templates.

### Deliverables

- Ingredient requests must prioritize and, when requested, restrict to valid
  Ingredient concepts. Clinical formulations must not be presented as if they
  satisfy ingredient scope.
- Remove lexical near-matches such as apraclonidine for clonidine through
  deterministic term, vocabulary, domain, and concept-class constraints.
- Preserve bounded initial retrieval, but allow the user to search/page the
  broader candidate universe and stage policy changes across pages.
- Show and enforce active result constraints rather than treating them as
  assistant prose.
- Add regression coverage for atomoxetine, guanfacine, clonidine, viloxazine,
  and explicit exclusions.

### Guardrails

A retrieval slice is not evidence that a concept set is complete. No concept
policy is inferred merely because a candidate matched a search term.

## 3. Reusable concept-set asset handoff

Complete the remaining attachment path without recreating the normal Atlas
concept-set editor.

### Deliverables

- Let a cohort-plan slot attach an existing saved concept set as an explicit
  user action, with intended criterion role and domain visible for review.
- Persist the exact expression snapshot/checksum accepted for the cohort plan.
- Distinguish the linked source asset from the immutable snapshot used by the
  generated cohort definition.
- Preserve normal standalone concept-set editing; later edits must not silently
  modify a saved or reviewed cohort plan.

### Boundary

Archived plans remain audit-retained and non-resumable. Add restore only if
real use demonstrates a need; do not expand this sprint with a restore UI by
default.

## 4. Controlled expansion of computable cohort projections

Extend only one declared Circe projection template at a time, guided by the
reference cohorts in `docs/evaluation/phenotype_make_computable/reference_set/`.

### Ordered templates

1. Generalize supporting Condition evidence to a Condition primary index. This
   enables symptom/diagnosis confirmation windows such as transverse myelitis.
2. Add deterministic repeated-event or confirmation-count handling where an
   explicit Circe projection and review surface can be tested.
3. Allow one concept-set asset to be bound across Condition and Observation
   occurrences, needed for rheumatoid-arthritis-style definitions.

The current Condition+overlapping-Visit and Drug+supporting-Condition templates
remain supported fast paths.

### Explicitly deferred

Alternate entry paths, nested Boolean groups, complex recurrence/era logic,
external cohorts, and advanced Circe constructs remain review-only or
unsupported until each has its own template, tests, and user-facing capability
boundary.

## 5. CIPHER and source-informed conversion foundation

Resume the broader conversion plan only after the meeting demo and terminology
retrieval work are stable.

### Deliverables

- Deterministic phenotype-source cards, immutable source snapshots, and
  conversion-readiness assessment.
- Traceable use of non-computable source phenotypes as evidence for a new,
  review-gated computable plan.
- One source-informed composition template at most in this sprint.
- Reference-set tests covering source fidelity, mapping/readiness outcomes, and
  the prohibition on automatic policy approval.

### Guardrails

CIPHER codes, mappings, and narrative are evidence—not approved OMOP concept
policy or executable Circe logic. `phenotype_make_computable` remains the sole
emitter after explicit scope, policy, binding, and logic review.

## 6. Quality and release discipline

- Add focused automated smoke coverage for the local demo profile, feature
  permissions, migration, and the three meeting stories.
- Keep the sandbox manifest/runbook synchronized with exact source tags,
  commits, environment prerequisites, and tested commands.
- Record model identifier/version and inference settings when a live ACP/LLM
  path is demonstrated.
- Create a new release checkpoint only after the documented demo can be
  reproduced from a clean local setup.

## Cross-cutting non-negotiables

- Atlas browser traffic goes only to WebAPI; ACP/MCP and all credentials remain
  server-side.
- No PHI/PII is sent to an LLM.
- Concept-set asset, criterion binding, and cohort logic remain separate models.
- No full large concept expansion is sent to an LLM.
- No Circe draft is emitted until every required concept-set policy and cohort
  logic decision is explicitly confirmed.
- Reference cohorts are development evidence, not clinical gold standards.

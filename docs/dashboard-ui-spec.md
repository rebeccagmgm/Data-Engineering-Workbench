# Data Engineering Workbench Read-only Dashboard UI Spec

## Purpose

`case-dashboard-generator` is a read-only generated view over Case source files. It is not the Workbench itself, and it must not become a project management system. Its job is to help the user open one page each day and answer:

- Which Cases deserve attention now?
- Which cards are waiting on me, Codex, a partner, an approver, or a platform?
- Which actions are done but not verified?
- Which claims are candidate, trusted, stale, or rejected?
- Which trusted claims lack evidence?
- Which evidence only proves historical/test state, not production or downstream-visible truth?
- Which Cases are closeout candidates?
- Which lessons are worth later promotion?

## Global Dashboard

### Question Answered

The global dashboard answers: "What should I look at first today, across all Cases?"

It must not show every field from every Case. It should show action-bearing queues only.

### Layout

1. Header
   - Generator name: `case-dashboard-generator`
   - Generated time
   - Source root
   - Validation summary: Error / Warning / Info counts
   - Explicit note: "Generated view. Edit source files, not this page."
   - Explicit local-only warning: "Local-only generated view. Do not send externally without redaction."

2. Top Risks
   - Highest-priority trust and verification risks using fixed explainable rules.
   - These appear before actions when they affect current conclusion or next action.
   - Each item must show Case, card or claim, risk reason, affected decision/action, and source ref.

3. Top Actions
   - Highest-priority actionable items using fixed explainable rules.
   - Each item must show Case, card or claim, owner, reason, next action, and missing evidence or expected signal.

4. Waiting By Owner
   - Lanes: `me`, `Codex`, `partner`, `approver`, `platform`, `unknown`.
   - Each lane lists cards with `waiting_on`, `expected_signal`, `blocked_since`, `next_touch_at`, and current risk.

5. Verification Gaps
   - `execution_state=done` with `verification_state=pending`
   - `execution_state=done` with `verification_state=failed`
   - `verification_state=passed` without evidence refs is a red risk.

6. Trust Gaps
   - Trusted claims without evidence.
   - Explicit prod/downstream claims using historical/test evidence.
   - Unknown-scope claims used by current conclusion or next action.
   - Candidate claims referenced by `next_action` or current conclusion.

7. Closeout Candidates
   - Cases that appear structurally near closeout.
   - Cases with closeout draft gaps.
   - Cases with learning candidates that cite cards/evidence.

### Fields Used

- From `case.yaml`: `case_id`, `title`, `mode`, `status`, `phase`, `owner`, `updated_at`, `current_conclusion`, `current_focus`, `current_blocker`, `next_action`, `claims`, `open_card_refs`, `asset_refs`, `run_refs`.
- From card frontmatter: `id`, `kind`, `title`, `domain`, `capability`, `owner`, `execution_state`, `verification_state`, `priority`, `env`, `external_dependency`, `exit_criteria`, `verification_method`, `evidence_refs`, `updated_at`.
- From evidence sidecar: `evidence_id`, `kind`, `title`, `observed_at`, `environment`, `source`, `supports`, `summary`, `limitations`, `asset_refs`, `run_refs`.
- From optional claim fields: `claim_scope.truth_environment`, `claim_scope.time_scope`.
- From optional card fields: `scope_status`.
- From `events.md`: structured event headings and bullet summaries only.
- From `closeout.md`: presence of `Change`, `Trust`, and `Learning` sections, plus whether each section cites known card/claim/evidence/asset/run refs.

### Red Risks

- A trusted claim has no `evidence_refs`.
- A passed verification card has no `evidence_refs`.
- An explicit prod or downstream claim is supported only by `test` or `historical` evidence.
- A claim used by current conclusion or next action has missing/unknown claim scope.
- A candidate claim is used as current conclusion or next action without warning.
- A waiting card lacks `waiting_on` or `expected_signal`.
- A done card has `verification_state=pending` and no `verification_method`.
- A failed verification card is not visible in the top-level risk area.

### Cannot Display As Trusted Complete

- `execution_state=done` by itself.
- Horae SUCCESS by itself.
- API 200, save success, or submitted request by itself.
- Historical notes, plans, or analysis by themselves.
- Test evidence for production/downstream claims.
- A closeout draft without Trust citations.

## Case Detail Page

### Question Answered

The Case detail page answers: "What is the current state of this Case, what blocks it, and what evidence supports its conclusions?"

### Layout

1. Case Header
   - Case title, status, phase, mode, owner, updated_at.
   - Mode badge: `historical_replay`, `active`, or other known modes.
   - If mode is `historical_replay`, show a persistent warning: "Historical replay does not prove current platform truth."

2. Current State Strip
   - Current conclusion summary.
   - Current focus card.
   - Current blocker.
   - Next action.

3. Attention Lanes
   - `blocked`
   - `waiting`
   - `done_not_verified`
   - `failed_verification`
   - `trust_gap`
   - `closeout_candidate`

4. Claims And Evidence
   - Claims grouped by status: trusted, candidate, stale, rejected.
   - Each claim shows evidence refs, source refs, last confirmed time, and environment limitations derived from evidence.

5. Cards Table
   - Sorted by attention lane first, then priority, then updated_at.
   - Columns: card, kind, owner, execution_state, verification_state, waiting_on, next_touch_at, evidence count, risk marker.

6. Recent Events
   - Reverse chronological events.
   - Each event should show what changed: claim, card, blocker, or evidence.

7. Closeout Preview
   - Shows Change / Trust / Learning section presence.
   - Shows missing citation warnings.

### Fields Used

All global dashboard fields, plus:

- `current_focus.card_ref`
- `current_blocker.card_ref`
- `next_action.card_ref`
- claim `last_confirmed_at` and `expires_at`
- card `input_refs`
- card `external_dependency.dependency_state`
- card `external_dependency.unblock_hypothesis`

### Red Risks

- `mode=historical_replay` and the Case is shown without historical warning.
- Current conclusion references a candidate or stale claim without a visible warning.
- Current blocker references a missing card.
- `open_card_refs` includes a missing card file.
- A card has `execution_state=waiting` but no owner/waiting party.
- A claim has `status=trusted` but all evidence is historical-only.

### Cannot Display As Trusted Complete

- A Case with open blocker cards.
- A Case whose current conclusion depends on candidate claims.
- A Case with failed verification cards affecting current scope.
- A Case with unknown current scope for cards that affect closeout.
- A historical replay Case unless the UI labels it as historical.
- A Case with closeout `Change` but no `Trust`.

## Card Detail Panel

### Question Answered

The card detail panel answers: "What does this card require, who or what is blocking it, and what evidence can verify it?"

This can be a side panel or a detail route. It remains read-only.

### Layout

1. Card Header
   - ID, title, kind, domain, owner, priority.
   - Execution and verification states shown as separate badges.

2. Action Contract
   - Capability.
   - Exit criteria.
   - Verification method.
   - Allowed actions and forbidden actions.

3. Dependency Block
   - dependency_state
   - waiting_on
   - expected_signal
   - blocked_since
   - next_touch_at
   - unblock_hypothesis

4. Evidence Links
   - evidence_refs with environment and limitations summaries.
   - Missing evidence warning when verification requires readback.

5. Source Links
   - claim refs, asset refs, run refs, source refs.

### Fields Used

- Card frontmatter only.
- Evidence sidecars referenced by `evidence_refs`.
- Claims referenced by `input_refs.claim_refs`.

The first version must not infer card state from Markdown body sections such as `## 结果`.

### Red Risks

- `execution_state=done` and `verification_state=pending`.
- `execution_state=done` and `verification_state=failed`.
- `verification_state=passed` without evidence.
- `exit_criteria` missing on task cards.
- `verification_method` missing on task cards.
- `forbidden_actions` missing on cards that touch prod, approval, or external communication.
- Waiting card has no `expected_signal`.

### Cannot Display As Trusted Complete

- Any card with `verification_state!=passed`.
- Any card with `verification_state=passed` but missing evidence.
- Any push/DDL/data-quality card verified only by a plan or analysis document.
- Any prod-affecting card whose only evidence is test or historical.

## Evidence Detail Panel

### Question Answered

The evidence detail panel answers: "What does this evidence prove, what does it not prove, and which claims/cards does it support?"

It must not become a log viewer. It should summarize metadata and link to the artifact path.

### Layout

1. Evidence Header
   - evidence_id, title, kind, observed_at, environment, source.

2. Supports
   - claim_refs
   - card_refs

3. Scope
   - summary
   - limitations
   - environment warnings
   - asset_refs
   - run_refs

4. Artifact
   - artifact_path
   - recorded_by

### Fields Used

- Evidence sidecar fields only.
- Claim and card reverse references derived from sidecar `supports`.

### Red Risks

- Evidence has no `supports.claim_refs` and no `supports.card_refs`.
- Evidence has no `limitations`.
- Evidence `environment=historical` supports a current prod claim.
- Evidence `environment=test` supports a downstream_actual claim.
- Evidence artifact path is missing.

### Cannot Display As Trusted Complete

- A plan, analysis, or implementation note by itself.
- A historical report as current platform truth.
- A test readback as production or downstream actual visibility.
- Evidence that only says a task ran, when the claim is about data correctness or downstream consumption.

## Local-only And Export Boundary

The generated dashboard is local-only by default. It may display:

- `source_root`
- `source_path`
- `artifact_path`
- internal table names in `asset_refs`
- scheduler or platform IDs in `run_refs`
- raw material locations

This is useful for local daily work, but the generated page is not an external report. If a future export/share mode exists, it must be a separate redaction mode that masks absolute paths, internal locations, credentials, internal hostnames, and any non-approved details. Export/share mode is out of scope for the first read-only dashboard.

## Closeout And Learning Page

### Question Answered

The closeout page answers: "Can this Case be closed, and which learning candidates deserve promotion?"

### Layout

1. Closeout Readiness
   - no open blockers
   - no failed verification affecting scope
   - no trusted claim without evidence
   - no current conclusion based on candidate/stale claim
   - closeout has Change / Trust / Learning sections

2. Change
   - Assets, run refs, cards, and decisions changed or evaluated.

3. Trust
   - Claims and evidence supporting delivery.
   - Residual risks.

4. Learning
   - Candidate learnings.
   - Required citation to card/event/evidence.
   - Suggested destination: stay in Case, promotion-inbox, agent-kb, Skill, CLI gap, or eval case.

### Fields Used

- `closeout.md` section presence and cited refs.
- Case claims.
- Cards and evidence referenced by closeout text or frontmatter.
- Events of type `learning_candidate` if structured.

### Red Risks

- Closeout exists but Trust section has no evidence refs.
- Learning has no card/evidence/event citation.
- Historical replay learning is phrased as current production fact.
- Closeout says done while failed verification cards remain in scope.

### Cannot Display As Trusted Complete

- A closeout draft marked as final without user confirmation.
- A Case with unresolved blocker cards.
- A Case where Trust is narrative-only and not evidence-backed.
- A Case where learning candidates are promoted without reuse or verification.

## Visual Rules

- Use separate badges for `execution_state` and `verification_state`.
- Green is allowed only when the relevant verification is passed and evidence-backed.
- Candidate, stale, historical, and unknown states must never use green.
- Failed verification and trust gaps are red.
- Waiting and pending verification are amber.
- Historical replay uses a persistent neutral warning style.
- Counts alone are insufficient; every risk count must link to the source Case/card/claim/evidence.

## Empty And Error States

- If no Cases exist, show: "No Case source files found."
- If a Case cannot be parsed, show the source path and validation errors.
- If evidence refs point to missing sidecars, show red trust gap rows.
- If `events.md` has no structured events, do not infer from prose; show "No structured events available."
- If `closeout.md` is missing, show closeout readiness as "not started", not failure.

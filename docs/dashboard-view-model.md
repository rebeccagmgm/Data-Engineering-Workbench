# Dashboard View Model

## Boundary

This document defines the read-only view model for `case-dashboard-generator`. It is a product contract, not an implementation plan.

The view model is derived from source files:

- `cases/*/case.yaml`
- `cases/*/cards/*.md` frontmatter
- `cases/*/evidence/*.yml`
- `cases/*/events.md` structured event blocks
- `cases/*/closeout.md` fixed sections

The first version does not infer state from Markdown body prose.

## Source Objects

### CaseSource

Fields:

- `case_id`
- `title`
- `mode`
- `status`
- `phase`
- `owner`
- `created_at`
- `updated_at`
- `source_root`
- `current_conclusion.summary`
- `current_conclusion.claim_refs`
- `current_focus.card_ref`
- `current_focus.reason`
- `current_blocker.card_ref`
- `current_blocker.summary`
- `next_action.summary`
- `next_action.card_ref`
- `claims`
- `open_card_refs`
- `asset_refs`
- `run_refs`

### CardSource

Fields:

- `id`
- `kind`
- `title`
- `domain`
- `capability`
- `owner`
- `execution_state`
- `verification_state`
- `priority`
- `env`
- `input_refs`
- `external_dependency`
- `exit_criteria`
- `verification_method`
- `allowed_actions`
- `forbidden_actions`
- `evidence_refs`
- `updated_at`

### ClaimSource

Fields:

- `claim_id`
- `statement`
- `status`
- `claim_scope.truth_environment`
- `claim_scope.time_scope`
- `claim_scope.notes`
- `source_refs`
- `evidence_refs`
- `last_confirmed_at`
- `expires_at`

Allowed statuses:

- `candidate`
- `trusted`
- `rejected`
- `stale`

`claim_scope.truth_environment` is the only reliable way to decide whether a claim is about `test`, `prod`, `downstream_actual`, `historical`, or `unknown`. The dashboard must not infer claim scope from `statement` text. If `claim_scope` is missing, treat the claim scope as `unknown` and emit a Warning, not an Error.

Allowed `claim_scope.truth_environment` values:

- `test`
- `prod`
- `downstream_actual`
- `historical`
- `unknown`

`unknown` cannot be displayed as production-ready or downstream-trusted.

### EvidenceSource

Fields:

- `evidence_id`
- `kind`
- `title`
- `observed_at`
- `environment`
- `source`
- `artifact_path`
- `supports.claim_refs`
- `supports.card_refs`
- `summary`
- `limitations`
- `asset_refs`
- `run_refs`
- `recorded_by`

Preferred future fields:

- `truth_environment`
- `consumer_view`
- `evidence_scope.proves`
- `evidence_scope.does_not_prove`

If preferred fields are absent, the dashboard may show warnings, but it must not infer them from prose.

### EventSource

Fields derived only from structured event headings:

- `event_date`
- `event_type`
- `summary`
- `source`
- `affected_refs`

For the current sample, headings such as `2026-06-22 evidence_readback` are valid structured event headers.

### CloseoutSource

Fields:

- `exists`
- `is_draft`
- `has_change_section`
- `has_trust_section`
- `has_learning_section`
- `change_refs`
- `trust_refs`
- `learning_refs`
- `residual_risks_present`
- `user_confirmed`

`user_confirmed` must be false unless a future structured marker explicitly says otherwise.

## Derived View Objects

### DashboardCase

Fields:

- `case_id`
- `title`
- `mode`
- `status`
- `phase`
- `owner`
- `updated_at`
- `current_conclusion_summary`
- `current_focus_card`
- `current_blocker_card`
- `next_action_card`
- `next_action_summary`
- `attention_lanes`
- `top_action_reason`
- `risk_counts`
- `closeout_readiness`
- `source_path`

### DashboardCard

Fields:

- `case_id`
- `card_id`
- `title`
- `kind`
- `domain`
- `owner`
- `priority`
- `execution_state`
- `verification_state`
- `dependency_state`
- `waiting_on`
- `expected_signal`
- `blocked_since`
- `next_touch_at`
- `exit_criteria_count`
- `verification_method_count`
- `evidence_count`
- `scope_status`
- `attention_lane`
- `risk_level`
- `risk_reasons`
- `source_path`

### DashboardClaim

Fields:

- `case_id`
- `claim_id`
- `statement`
- `status`
- `evidence_refs`
- `evidence_count`
- `evidence_environments`
- `claim_scope_truth_environment`
- `last_confirmed_at`
- `expires_at`
- `is_used_by_current_conclusion`
- `is_used_by_next_action`
- `risk_level`
- `risk_reasons`

### DashboardEvidence

Fields:

- `case_id`
- `evidence_id`
- `kind`
- `title`
- `observed_at`
- `environment`
- `source`
- `artifact_path`
- `supported_claims`
- `supported_cards`
- `limitations`
- `asset_refs`
- `run_refs`
- `risk_level`
- `risk_reasons`

### DashboardHealth

Fields:

- `case_count`
- `active_case_count`
- `stale_waiting_count`
- `unverified_done_count`
- `failed_verification_count`
- `trusted_claim_without_evidence_count`
- `candidate_claim_used_by_next_action_count`
- `historical_or_test_evidence_for_current_truth_count`
- `evidence_without_refs_count`
- `closeout_candidate_count`
- `validation_error_count`
- `validation_warning_count`
- `validation_info_count`

## Scope Rules

Scope determines whether a card or claim can affect current Case readiness. It must be explicit or derived from structural fields, never from prose.

### Card Scope

Optional card field:

- `scope_status: in_scope | out_of_scope | historical_only | obsolete | unknown`

Default derivation when `scope_status` is absent:

- Card IDs listed in `case.yaml.open_card_refs` are `in_scope`.
- Cards with `execution_state=obsolete` or `execution_state=cancelled` are `out_of_scope`.
- Cards not listed in `open_card_refs` are `out_of_scope` for readiness calculations but can still appear in full Case history.
- In `mode=historical_replay`, cards with `env=historical` remain in-scope for replay analysis, but they are not current platform proof.

Meaning:

- `in_scope`: affects current Case readiness.
- `out_of_scope`: visible in history, excluded from readiness.
- `historical_only`: can support historical replay findings, but cannot support current prod/downstream completion.
- `obsolete`: excluded from readiness and shown as superseded.
- `unknown`: warning; do not use for closeout-ready decisions.

### Claim Scope

Optional claim field:

- `claim_scope.truth_environment: test | prod | downstream_actual | historical | unknown`

Default derivation when absent:

- `unknown`

Trust gap severity:

- If `claim_scope.truth_environment` is `prod` or `downstream_actual` and all supporting evidence is `test`, `historical`, `plan`, or `analysis`, emit Error.
- If `claim_scope.truth_environment` is missing or `unknown`, emit Warning: `claim_scope_unknown`.
- Do not infer prod/downstream scope from the claim statement text.

### Closeout Scope

Derived Case closeout scope:

- `mode=historical_replay` -> `replay_only`
- otherwise -> `delivery`

For `delivery` closeout:

- failed in-scope verification cards block closeout.
- historical-only evidence cannot prove current prod/downstream truth.

For `replay_only` closeout:

- failed historical cards may be acceptable findings if the closeout Trust section cites them as residual risks or historical gaps.
- unresolved decision/blocker cards still block final closeout.
- replay closeout must be visually distinct from delivery completion.

## Attention Lanes

Lanes are derived. There is no lanes file.

### `blocked`

A card enters `blocked` when:

- `execution_state=blocked`, or
- `kind=blocker` and `execution_state` is not `done` or `cancelled`.

### `waiting`

A card enters `waiting` when:

- `execution_state=waiting`.

Subgroup by `external_dependency.waiting_on`:

- `me`
- `Codex`
- `partner`
- `approver`
- `platform`
- `unknown`

The source value can remain Chinese/freeform, but the view should map common values into these groups. Unknown values must stay visible.

### `done_not_verified`

A card enters `done_not_verified` when:

- `execution_state=done`
- `verification_state=pending`

### `failed_verification`

A card enters `failed_verification` when:

- `verification_state=failed`

### `trust_gap`

A case or claim enters `trust_gap` when:

- trusted claim has no evidence refs
- passed card has no evidence refs
- explicit prod/downstream claim scope only has test or historical evidence
- claim scope is unknown and the claim is used by current conclusion or next action
- candidate claim is used by current conclusion or next action

### `closeout_candidate`

A case enters `closeout_candidate` when:

- no open blocker card is in scope
- no failed verification card affects current scope
- current conclusion does not depend on candidate/stale claim
- all trusted claims have evidence
- closeout is missing or draft or lacks Trust citations

The current Jinshida replay Case does not qualify for final closeout because it has a historical boundary blocker and a user decision about current readback. Its failed verification cards are valid historical findings, not delivery-complete proof.

## Top Risks And Top Actions

The dashboard must separate risk prevention from action prompting. A user should not be nudged into action before seeing a trust gap that affects the current conclusion or next action.

### Top Risks

Top Risks are fixed-rule findings, not a score. The first matching rule wins, then priority and updated time break ties.

1. `trust_gap` affects `current_conclusion` or `next_action`.
2. Failed in-scope verification.
3. Passed verification without evidence.
4. Explicit prod/downstream claim backed only by test/historical evidence.
5. Current conclusion uses candidate/stale claim.
6. `claim_scope` is unknown for a claim used by current conclusion or next action.

Each Top Risk item must expose:

- `matched_rule`
- `matched_reason`
- `source_ref`

### Top Actions

Top Actions are fixed-rule actionable items after Top Risks are shown.

1. Owner is user/me and next action is explicit.
2. Card is `done_not_verified` and has `verification_method`.
3. Card is `waiting` and `next_touch_at` is due or overdue.
4. Card is `blocked` and has `unblock_hypothesis`.
5. Case is a `closeout_candidate`.

Each Top Action item must expose:

- `matched_rule`
- `matched_reason`
- `source_ref`

No hidden score may decide either list.

## Risk Levels

### Error

Error means the view may mislead the user if not surfaced prominently.

Examples:

- trusted claim has no evidence
- passed verification has no evidence
- current conclusion uses candidate/stale claim
- explicit prod/downstream claim is backed only by test/historical evidence
- missing source card referenced by `current_focus`, `current_blocker`, `next_action`, or `open_card_refs`

### Warning

Warning means the item can be displayed, but it belongs in a risk queue.

Examples:

- waiting card lacks `next_touch_at`
- done card has pending verification
- failed verification remains in scope
- claim scope is missing or unknown
- evidence lacks limitations
- evidence lacks preferred `truth_environment`
- closeout is draft

### Info

Info means quality or completeness issue.

Examples:

- optional `domain_path` is absent
- evidence lacks `consumer_view`
- no structured events found
- closeout learning candidates not yet routed

## Trust Rules

### Claim Trust

A claim can display as trusted only if:

- `status=trusted`
- it has at least one `evidence_ref`
- the referenced evidence exists

Even then, the dashboard must show claim scope and evidence environment. If all evidence is historical, the claim is trusted only within historical scope. If claim scope is unknown, the dashboard may show `status=trusted` as source data, but must not show it as prod/downstream trusted.

### Card Trust

A card can display as verified only if:

- `execution_state=done`
- `verification_state=passed`
- `evidence_refs` is not empty

If a card is done but pending or failed, it must not be green.

### Case Trust

A Case can display as closeout-ready only if:

- no blocking card remains open
- no failed verification card remains in current scope
- current conclusion does not depend on candidate/stale claims
- current conclusion does not depend on unknown-scope claims for prod/downstream action
- trusted claims have evidence
- closeout Trust section exists and cites evidence/claims/cards/assets/runs

### Evidence Scope

Evidence cannot prove more than its environment and kind allow.

- `historical` proves historical material, not current state.
- `test` proves test state, not production or downstream truth.
- `plan`, `analysis`, `atomic_note`, and `implementation_note` support reasoning, but do not replace readback.
- A scheduler success supports run state, not business data correctness.

## Local-only And Export Boundary

The generated dashboard is local-only by default. It may contain absolute paths, internal table names, task IDs, raw material locations, and evidence artifact paths.

View model fields that may expose sensitive local or internal context:

- `source_path`
- `source_root`
- `artifact_path`
- `asset_refs`
- `run_refs`
- `source_refs`

Default behavior:

- show these fields only for local use;
- mark generated output as not suitable for external sharing;
- preserve exact paths so the local user can return to source files.

Future export/share mode is a separate product mode and must include redaction rules before any generated page is sent outside the local workspace. Redaction mode must remove or mask absolute paths, internal hostnames, sensitive raw material locations, credentials, and any non-approved internal details. It is not part of the first read-only dashboard.

## Sample Mapping: Jinshida Replay

Expected derived highlights from `CASE-20260611-jinshida-market-push`:

- `B-001` appears in waiting, grouped under user/me.
- `Q-001` appears as a user decision item.
- `T-003` and `T-004` appear in failed verification.
- `T-005` appears in done_not_verified.
- `C-005` appears as candidate with no evidence.
- `C-002` appears as stale and must not support current action.
- Evidence `EV-20260622-prod-verify` and `EV-20260625-actual-logic` are historical and must show "does not prove current platform state."
- The Case is not closeout-ready as final, because closeout is explicitly a historical replay draft and current readback remains a decision.

## Non-derived Content

The view model must not derive any state from:

- Markdown body prose under cards.
- Natural language in `notes.md`.
- Freeform closeout text without citations.
- Raw attachments.
- Chat logs.

Those sources may be linked, but they do not drive dashboard state in the first version.

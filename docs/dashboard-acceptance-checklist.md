# Dashboard Acceptance Checklist

This checklist defines acceptance for the read-only Dashboard product design. It is not an implementation task list.

## Global Constraints

- [ ] No editable UI is specified.
- [ ] No drag-and-drop board is specified.
- [ ] No database is required.
- [ ] No server is required.
- [ ] No platform synchronization is required.
- [ ] No fixed business process menu is required.
- [ ] Markdown/YAML source files remain source of truth.
- [ ] Generated cache or HTML is disposable and not manually edited.
- [ ] The first version reads only structured data, not Markdown body prose.
- [ ] Generated output is local-only by default.
- [ ] Any external sharing/export requires a future redaction mode.
- [ ] The UI never treats `done` as `verified`.
- [ ] The UI never treats `candidate` as `trusted`.

## Global Dashboard Acceptance

### Page Question

- [ ] The page clearly answers: "What should I advance first today?"
- [ ] It shows Top Risks before Top Actions.
- [ ] Top Risks use fixed rule explanations.
- [ ] Top Actions use fixed rule explanations.
- [ ] It shows waiting items grouped by owner/waiting party.
- [ ] It shows done-but-not-verified cards.
- [ ] It shows trust gaps.
- [ ] It shows closeout candidates.

### Field Use

- [ ] Uses `case.yaml` for Case state.
- [ ] Uses card frontmatter for card state.
- [ ] Uses evidence sidecars for evidence scope.
- [ ] Uses `claim_scope.truth_environment` when judging prod/downstream trust gaps.
- [ ] Treats missing claim scope as Warning, not guessed Error.
- [ ] Uses `scope_status` or structural scope rules when judging current scope.
- [ ] Uses structured event headings only.
- [ ] Uses closeout section presence and citations only.

### Red Risks

- [ ] Trusted claim without evidence appears as Error.
- [ ] Passed verification without evidence appears as Error.
- [ ] Explicit prod/downstream claim backed only by test/historical evidence appears as Error.
- [ ] Unknown claim scope used by current conclusion or next action appears as Warning.
- [ ] Candidate claim used by current conclusion or next action appears as Error.
- [ ] Waiting card without expected signal appears as Warning or Error based on scope.

### Cannot Show As Trusted Complete

- [ ] `execution_state=done` alone is not green.
- [ ] Historical replay state is not shown as current platform truth.
- [ ] Test evidence is not shown as prod/downstream proof.
- [ ] Closeout draft is not shown as final.

## Case Detail Acceptance

### Page Question

- [ ] The page clearly answers: "What is this Case's current state and why?"
- [ ] Current conclusion, current focus, blocker, and next action are visible above the fold.
- [ ] Historical replay mode has a persistent warning.
- [ ] Attention lanes are derived and visible.
- [ ] Claims are grouped by status.
- [ ] Evidence environment and limitations are visible.

### Field Use

- [ ] Uses `current_conclusion.claim_refs`.
- [ ] Uses `current_focus.card_ref`.
- [ ] Uses `current_blocker.card_ref`.
- [ ] Uses `next_action.card_ref`.
- [ ] Uses `claims[].status`.
- [ ] Uses card and evidence refs for cross-links.

### Red Risks

- [ ] Missing referenced card is Error.
- [ ] Current conclusion using candidate/stale claim is Error.
- [ ] Failed verification card in current scope is Error.
- [ ] Trusted claim with only historical evidence is at least Warning and may be Error if presented as current truth.
- [ ] Missing card scope for closeout-affecting cards appears as Warning.

### Cannot Show As Trusted Complete

- [ ] Case with open blocker is not closeout-ready.
- [ ] Case with failed verification in scope is not closeout-ready.
- [ ] Case with candidate current conclusion is not closeout-ready.
- [ ] Case with Trust section lacking evidence citations is not closeout-ready.

## Card Detail Acceptance

### Page Question

- [ ] The page clearly answers: "What does this card need, who is responsible, and how can it be verified?"
- [ ] Execution and verification states are separate badges.
- [ ] Exit criteria are visible.
- [ ] Verification method is visible.
- [ ] Waiting fields are visible when present.
- [ ] Evidence refs are visible and linked.

### Field Use

- [ ] Uses card frontmatter only for state.
- [ ] Uses referenced evidence sidecars for evidence details.
- [ ] Uses referenced claims for claim context.
- [ ] Does not parse card body text for status.

### Red Risks

- [ ] Done but pending appears in risk style.
- [ ] Done but failed appears in red.
- [ ] Passed without evidence appears as Error.
- [ ] Task without exit criteria appears as Warning.
- [ ] Task without verification method appears as Warning.
- [ ] Waiting card without `expected_signal` appears as Warning.

### Cannot Show As Trusted Complete

- [ ] Card with `verification_state=pending` is not verified.
- [ ] Card with `verification_state=failed` is not verified.
- [ ] Card with no evidence is not verified even if status says passed.
- [ ] Card touching prod is not verified by plan/analysis only.

## Evidence Detail Acceptance

### Page Question

- [ ] The page clearly answers: "What does this evidence prove and not prove?"
- [ ] Evidence supports are visible.
- [ ] Evidence limitations are visible.
- [ ] Environment is visible.
- [ ] Artifact path is visible.

### Field Use

- [ ] Uses evidence sidecar only.
- [ ] Uses `supports.claim_refs`.
- [ ] Uses `supports.card_refs`.
- [ ] Uses `limitations`.
- [ ] Uses `asset_refs` and `run_refs`.

### Red Risks

- [ ] Evidence without supports appears as Warning or Error.
- [ ] Evidence without limitations appears as Warning.
- [ ] Historical evidence supporting current fact appears as Error.
- [ ] Test evidence supporting prod/downstream appears as Error.
- [ ] Missing claim scope prevents hard prod/downstream trust-gap inference.
- [ ] Missing artifact path appears as Warning.

### Cannot Show As Trusted Complete

- [ ] Analysis document is not readback proof.
- [ ] Plan document is not readback proof.
- [ ] Historical report is not current state proof.
- [ ] Scheduler success is not downstream data proof.

## Closeout And Learning Acceptance

### Page Question

- [ ] The page clearly answers: "Can this Case be closed, and what learning is worth keeping?"
- [ ] Change, Trust, and Learning section status is visible.
- [ ] Residual risks are visible.
- [ ] Learning candidates cite source cards/events/evidence.
- [ ] Suggested promotion destination is visible as recommendation only.

### Field Use

- [ ] Uses closeout section presence.
- [ ] Uses cited refs.
- [ ] Uses claim/evidence/card status.
- [ ] Uses structured learning events only if available.

### Red Risks

- [ ] Closeout with no Trust citations appears as Error.
- [ ] Learning with no citation appears as Warning.
- [ ] Historical learning phrased as current fact appears as Error.
- [ ] Closeout while failed verification remains in scope appears as Error.

### Cannot Show As Trusted Complete

- [ ] Draft closeout is not final.
- [ ] Unresolved blocker prevents closeout-ready.
- [ ] Narrative-only Trust does not count.
- [ ] Learning cannot be promoted without reuse or confirmation.

## Jinshida Sample Acceptance

For `CASE-20260611-jinshida-market-push`, the design should classify:

- [ ] `B-001` as waiting on user decision.
- [ ] `Q-001` as a user decision/question.
- [ ] `T-003` as failed verification.
- [ ] `T-004` as failed verification.
- [ ] `T-005` as done but verification pending.
- [ ] `C-005` as candidate with no evidence.
- [ ] `C-002` as stale.
- [ ] `EV-20260622-prod-verify` as historical evidence, not current platform proof.
- [ ] `EV-20260625-actual-logic` as historical evidence, not current platform proof.
- [ ] Case closeout as draft/historical, not final delivery complete.
- [ ] Failed historical cards as replay findings, not delivery-complete proof.

## Validation Severity Acceptance

- [ ] Error / Warning / Info are defined.
- [ ] Not all lint findings block dashboard generation.
- [ ] Error findings are prominently visible.
- [ ] Warnings are visible in risk queues.
- [ ] Info does not distract from action.

## Kill Criteria Acceptance

- [ ] The design includes Dashboard kill criteria.
- [ ] Kill criteria include daily usefulness.
- [ ] Kill criteria include stale/misleading dashboard risk.
- [ ] Kill criteria include maintenance burden.
- [ ] Kill criteria include evidence coverage.
- [ ] Kill criteria include no blocker or evidence gap discovered.

## Review Questions Before Implementation

- [ ] Which two or three Cases will be used for the first dashboard trial?
- [ ] Will `events.md` structured event parsing be required in version one, or can it be optional?
- [ ] Which card frontmatter fields become Error-level required fields?
- [ ] Should `claim_scope.truth_environment` be added to existing sample claims before implementation?
- [ ] Should preferred evidence fields `truth_environment`, `consumer_view`, and `evidence_scope` be required now or introduced as Warning first?
- [ ] Should `scope_status` be added to cards, or should version one rely on `open_card_refs` and execution states?
- [ ] Where should disposable generated artifacts live?

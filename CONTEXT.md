# Data Engineering Workbench

This context defines the language for a lightweight workbench that helps a data developer run real demand cases, track uncertainty, verify evidence, and distill reusable knowledge.

## Language

**Case**:
A bounded data-development demand space with its own current conclusion, cards, source material, evidence, blockers, and distillation candidates.
_Avoid_: task, project, document folder

**Source Pack**:
The raw intake layer for a Case, containing demand notes, flows, attachments, screenshots, chat records, and other unverified inputs.
_Avoid_: evidence, truth source, knowledge base

**Candidate Fact**:
A claim extracted from source material that may be useful but is not yet trusted.
_Avoid_: fact, verified conclusion

**Claim**:
A tracked statement the Case currently needs to prove, reject, or watch for staleness. A claim links source material to evidence and has a status such as candidate, trusted, rejected, or stale.
_Avoid_: loose note, raw chat conclusion

**Evidence**:
A time-stamped readback or confirmation that supports or limits a specific claim, with its source and environment made explicit.
_Avoid_: raw material, log dump

**Current Trusted Conclusion**:
The Case's latest actionable judgment after combining source material, analysis, evidence, and known limits.
_Avoid_: historical analysis, assumption

**Card**:
A small tracked unit inside a Case, such as a question, task, blocker, evidence note, decision, or distillation candidate.
_Avoid_: fixed workflow step

**Blocker**:
A card that records where progress is stuck, who or what it is waiting on, and how it can be unblocked or verified.
_Avoid_: todo, issue

**External Dependency**:
A tracked waiting relationship outside the immediate Case executor, such as approval, partner DDL sync, platform permission propagation, or downstream readback. It should have waiting_on, blocked_since, expected_signal, next_touch_at, and escalation information.
_Avoid_: vague waiting status

**AssetRef**:
A structured reference to a data asset touched by a Case, such as a table, dataset, wide table, API, topic, or target schema.
_Avoid_: asset name only inside prose

**RunRef**:
A structured reference to an execution or workflow instance, such as a scheduler task, scheduler run, flow application, QC ticket, or push execution.
_Avoid_: run id buried in evidence text

**Capability**:
A business-level ability the Case needs, such as checking a scheduling topic permission or reading a flow status, independent of the current CLI or manual implementation.
_Avoid_: command, button

**Workbench Knowledge Layer**:
The local runtime knowledge layer for reusable Case templates, workflow patterns, capability contracts, promotion candidates, and promotion logs.
In the MVP, this should behave mostly as a promotion inbox; richer directories are only populated after repeated real Case reuse.
_Avoid_: formal knowledge base, agent-kb copy

**Distillation Candidate**:
A possible reusable lesson extracted from a Case that still needs classification, routing, and future-use validation before becoming formal knowledge.
_Avoid_: knowledge, memory

**Promotion**:
The act of moving a validated distillation candidate into a more durable home such as agent-kb, a Workbench doc, a Skill, a CLI command, or an eval case.
_Avoid_: copy, dump

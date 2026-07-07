# Case Dashboard Generator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local, read-only `case-dashboard-generator` that derives a disposable dashboard from `cases/*` source files.

**Architecture:** A single Python CLI reads `case.yaml`, card frontmatter, evidence sidecars, optional `events.md`, and optional `closeout.md`; it builds a deterministic view model and writes `tmp/case-dashboard/index.html`. Source files remain the only truth, and generated output is disposable.

**Tech Stack:** Python 3.14, PyYAML, `unittest`, static HTML/CSS with no server and no JavaScript dependency.

## Global Constraints

- Read only source files under `cases/*`.
- Do not create an editable UI, database, server, platform sync, or hidden write path.
- Do not infer state from card Markdown body prose.
- Treat `done` and `verified` as separate states.
- Treat `candidate`, `stale`, `historical`, `test`, and `unknown` as non-green states.
- Write generated artifacts under ignored `tmp/case-dashboard/`.
- Keep exact `source_path` values in generated local output.
- Update root `CHANGELOG.md` for the material repository change.

---

### Task 1: Dashboard View Model Tests

**Files:**
- Create: `tests/test_case_dashboard_generator.py`

**Interfaces:**
- Consumes: planned `build_dashboard(source_root: Path, now: datetime | None = None) -> dict[str, Any]`
- Produces: failing behavioral tests for the Jinshida sample Case.

- [ ] **Step 1: Write failing tests**

```python
from datetime import datetime, timezone
from pathlib import Path
import unittest

from scripts.case_dashboard_generator import build_dashboard, render_dashboard_html


ROOT = Path(__file__).resolve().parents[1]


class CaseDashboardGeneratorTests(unittest.TestCase):
    def test_jinshida_sample_is_classified_into_attention_lanes(self):
        dashboard = build_dashboard(ROOT, now=datetime(2026, 7, 7, tzinfo=timezone.utc))

        self.assertEqual(dashboard["health"]["case_count"], 1)
        self.assertEqual(dashboard["health"]["failed_verification_count"], 2)
        self.assertEqual(dashboard["health"]["unverified_done_count"], 1)

        lanes = dashboard["cases"][0]["attention_lanes"]
        self.assertIn("B-001", lanes["waiting"])
        self.assertIn("T-003", lanes["failed_verification"])
        self.assertIn("T-004", lanes["failed_verification"])
        self.assertIn("T-005", lanes["done_not_verified"])

    def test_top_risks_precede_actions_and_explain_source_rules(self):
        dashboard = build_dashboard(ROOT, now=datetime(2026, 7, 7, tzinfo=timezone.utc))

        top_risk_sources = {item["source_ref"] for item in dashboard["top_risks"]}
        top_action_sources = {item["source_ref"] for item in dashboard["top_actions"]}

        self.assertIn("CASE-20260611-jinshida-market-push:T-003", top_risk_sources)
        self.assertIn("CASE-20260611-jinshida-market-push:T-004", top_risk_sources)
        self.assertIn("CASE-20260611-jinshida-market-push:B-001", top_action_sources)
        self.assertTrue(all(item["matched_rule"] for item in dashboard["top_risks"]))

    def test_rendered_html_is_local_only_and_orders_risks_before_actions(self):
        dashboard = build_dashboard(ROOT, now=datetime(2026, 7, 7, tzinfo=timezone.utc))
        html = render_dashboard_html(dashboard)

        self.assertIn("case-dashboard-generator", html)
        self.assertIn("Local-only generated view", html)
        self.assertLess(html.index("Top Risks"), html.index("Top Actions"))
        self.assertIn("T-005", html)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s tests -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.case_dashboard_generator'`.

### Task 2: Dashboard Generator Implementation

**Files:**
- Create: `scripts/case_dashboard_generator.py`

**Interfaces:**
- Produces: `build_dashboard(source_root: Path, now: datetime | None = None) -> dict[str, Any]`
- Produces: `render_dashboard_html(dashboard: Mapping[str, Any]) -> str`
- Produces: CLI `python scripts/case_dashboard_generator.py --source-root . --output tmp/case-dashboard/index.html`

- [ ] **Step 1: Implement parsing and lane derivation**

Use PyYAML for `case.yaml`, `cards/*.md` frontmatter, and `evidence/*.yml`. Derive lanes only from structured fields.

- [ ] **Step 2: Implement top risks and actions**

Include fixed-rule explanations for failed verification, passed-without-evidence, trusted-claim-without-evidence, done-not-verified, waiting, and user-owned question cards.

- [ ] **Step 3: Implement HTML rendering**

Render a local-only static dashboard with header, health counts, Top Risks, Top Actions, waiting lanes, verification gaps, trust gaps, and case summaries.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest discover -s tests -v`

Expected: PASS with 3 tests.

### Task 3: Generated Artifact And Changelog

**Files:**
- Modify: `CHANGELOG.md`
- Generate: `tmp/case-dashboard/index.html`

**Interfaces:**
- Consumes: `scripts/case_dashboard_generator.py`
- Produces: disposable local HTML for manual inspection.

- [ ] **Step 1: Generate dashboard**

Run: `python scripts/case_dashboard_generator.py --source-root . --output tmp/case-dashboard/index.html`

Expected: exit 0 and generated HTML under ignored `tmp/`.

- [ ] **Step 2: Update changelog**

Add a `2026-07-07 - case dashboard generator v0` entry recording files, decisions, open questions, and next steps.

- [ ] **Step 3: Verify**

Run:

```powershell
python -m unittest discover -s tests -v
python scripts/case_dashboard_generator.py --source-root . --output tmp/case-dashboard/index.html
rg -n "case-dashboard-generator|Top Risks|Top Actions|T-005|Local-only generated view" tmp/case-dashboard/index.html
```

Expected: tests pass, generator exits 0, and `rg` finds the expected dashboard markers.

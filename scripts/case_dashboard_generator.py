from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Mapping

import yaml


LANE_KEYS = [
    "blocked",
    "waiting",
    "done_not_verified",
    "failed_verification",
    "trust_gap",
    "closeout_candidate",
    "question",
]

WAITING_GROUPS = ["me", "Codex", "partner", "approver", "platform", "unknown"]

PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def build_dashboard(source_root: Path, now: datetime | None = None) -> dict[str, Any]:
    root = source_root.resolve()
    generated_at = now or datetime.now(timezone.utc)
    cases = [_build_case(case_dir, root) for case_dir in _case_dirs(root)]

    top_risks: list[dict[str, Any]] = []
    top_actions: list[dict[str, Any]] = []
    waiting_by_owner: dict[str, list[dict[str, Any]]] = {key: [] for key in WAITING_GROUPS}
    verification_gaps: list[dict[str, Any]] = []
    trust_gaps: list[dict[str, Any]] = []
    closeout_candidates: list[dict[str, Any]] = []

    for case in cases:
        top_risks.extend(case["top_risks"])
        top_actions.extend(case["top_actions"])
        verification_gaps.extend(case["verification_gaps"])
        trust_gaps.extend(case["trust_gaps"])
        if "closeout_candidate" in case["attention_lanes"]:
            closeout_candidates.append(case)
        for group, cards in case["waiting_by_owner"].items():
            waiting_by_owner[group].extend(cards)

    health = _build_health(cases)

    return {
        "generator": "case-dashboard-generator",
        "generated_at": generated_at.isoformat(),
        "source_root": str(root),
        "health": health,
        "top_risks": sorted(top_risks, key=_risk_sort_key),
        "top_actions": sorted(top_actions, key=_action_sort_key),
        "waiting_by_owner": waiting_by_owner,
        "verification_gaps": verification_gaps,
        "trust_gaps": trust_gaps,
        "closeout_candidates": closeout_candidates,
        "cases": cases,
    }


def render_dashboard_html(dashboard: Mapping[str, Any]) -> str:
    health = dashboard["health"]
    risk_rows = _render_rows(
        dashboard["top_risks"],
        ["risk_level", "source_ref", "matched_rule", "matched_reason"],
        empty="No top risks.",
    )
    action_rows = _render_rows(
        dashboard["top_actions"],
        ["owner_group", "source_ref", "matched_rule", "matched_reason", "next_action"],
        empty="No top actions.",
    )
    waiting_sections = "\n".join(
        _render_waiting_group(group, items)
        for group, items in dashboard["waiting_by_owner"].items()
        if items
    )
    verification_rows = _render_rows(
        dashboard["verification_gaps"],
        ["case_id", "card_id", "title", "execution_state", "verification_state", "risk_reasons"],
        empty="No verification gaps.",
    )
    trust_rows = _render_rows(
        dashboard["trust_gaps"],
        ["case_id", "source_ref", "risk_level", "risk_reasons"],
        empty="No trust gaps.",
    )
    case_sections = "\n".join(_render_case_summary(case) for case in dashboard["cases"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>case-dashboard-generator</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f8faf9;
      --panel: #ffffff;
      --ink: #17201b;
      --muted: #66736c;
      --line: #d9e1dc;
      --red: #b42318;
      --amber: #a15c07;
      --green: #147d55;
      --blue: #1d4e89;
      --surface: #eef4f1;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 "Segoe UI", Arial, sans-serif;
    }}
    header {{
      padding: 24px 32px 18px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }}
    main {{ padding: 20px 32px 40px; }}
    h1, h2, h3 {{ margin: 0; letter-spacing: 0; }}
    h1 {{ font-size: 24px; }}
    h2 {{ font-size: 18px; margin-bottom: 12px; }}
    h3 {{ font-size: 15px; margin-bottom: 8px; }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px 18px;
      margin-top: 14px;
      color: var(--muted);
      font-size: 13px;
    }}
    .notice {{
      margin-top: 14px;
      padding: 10px 12px;
      border-left: 4px solid var(--amber);
      background: #fff8e8;
      color: #4f3300;
    }}
    section {{
      margin-top: 18px;
      padding: 18px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .health {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
      gap: 10px;
    }}
    .metric {{
      min-height: 74px;
      padding: 12px;
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 6px;
    }}
    .metric strong {{ display: block; font-size: 22px; }}
    .metric span {{ color: var(--muted); font-size: 12px; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}
    th, td {{
      padding: 9px 8px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
    }}
    th {{ color: var(--muted); font-size: 12px; font-weight: 650; }}
    .badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      font-size: 12px;
      color: var(--muted);
    }}
    .error {{ color: var(--red); font-weight: 650; }}
    .warning {{ color: var(--amber); font-weight: 650; }}
    .ok {{ color: var(--green); font-weight: 650; }}
    .case-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
    }}
    .case-summary {{
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
    }}
    .case-summary p {{ margin: 8px 0 0; color: var(--muted); }}
    code {{ font-family: "Cascadia Mono", Consolas, monospace; }}
  </style>
</head>
<body>
  <header>
    <h1>{escape(str(dashboard["generator"]))}</h1>
    <div class="meta">
      <div>Generated: <code>{escape(str(dashboard["generated_at"]))}</code></div>
      <div>Source root: <code>{escape(str(dashboard["source_root"]))}</code></div>
      <div>Validation: <span class="error">{health["validation_error_count"]} errors</span>,
        <span class="warning">{health["validation_warning_count"]} warnings</span>,
        {health["validation_info_count"]} info</div>
    </div>
    <div class="notice">Generated view. Edit source files, not this page. Local-only generated view. Do not send externally without redaction.</div>
  </header>
  <main>
    <section>
      <h2>Health</h2>
      {_render_health(health)}
    </section>
    <section>
      <h2>Top Risks</h2>
      {risk_rows}
    </section>
    <section>
      <h2>Top Actions</h2>
      {action_rows}
    </section>
    <section>
      <h2>Waiting By Owner</h2>
      {waiting_sections or "<p>No waiting cards.</p>"}
    </section>
    <section>
      <h2>Verification Gaps</h2>
      {verification_rows}
    </section>
    <section>
      <h2>Trust Gaps</h2>
      {trust_rows}
    </section>
    <section>
      <h2>Cases</h2>
      <div class="case-grid">{case_sections or "<p>No Case source files found.</p>"}</div>
    </section>
  </main>
</body>
</html>
"""


def write_dashboard(source_root: Path, output: Path) -> dict[str, Any]:
    dashboard = build_dashboard(source_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dashboard_html(dashboard), encoding="utf-8")
    return dashboard


def _case_dirs(root: Path) -> list[Path]:
    cases_root = root / "cases"
    if not cases_root.exists():
        return []
    return sorted(path for path in cases_root.iterdir() if (path / "case.yaml").exists())


def _build_case(case_dir: Path, root: Path) -> dict[str, Any]:
    case_data = _read_yaml(case_dir / "case.yaml")
    cards = [_read_card(path) for path in sorted((case_dir / "cards").glob("*.md"))]
    evidence = [_read_evidence(path) for path in sorted((case_dir / "evidence").glob("*.yml"))]
    evidence_by_id = {item["evidence_id"]: item for item in evidence if item.get("evidence_id")}
    card_by_id = {card["id"]: card for card in cards if card.get("id")}
    case_id = case_data.get("case_id", case_dir.name)

    lanes = {key: [] for key in LANE_KEYS}
    waiting_by_owner: dict[str, list[dict[str, Any]]] = {key: [] for key in WAITING_GROUPS}
    top_risks: list[dict[str, Any]] = []
    top_actions: list[dict[str, Any]] = []
    verification_gaps: list[dict[str, Any]] = []
    trust_gaps: list[dict[str, Any]] = []
    validation = {"errors": [], "warnings": [], "info": []}

    open_card_refs = set(case_data.get("open_card_refs") or [])
    for card in cards:
        card["case_id"] = case_id
        card["in_current_scope"] = _is_card_in_scope(card, open_card_refs, case_data.get("mode"))
        card["attention_lane"] = _derive_card_lane(card)
        for lane in _derive_card_lanes(card):
            lanes[lane].append(card["id"])
        if card["execution_state"] == "waiting":
            waiting_by_owner[_owner_group(card)].append(_card_action_summary(card, case_id))
        if _is_failed_verification(card):
            top_risks.append(
                _finding(
                    case_id,
                    card["id"],
                    "Error",
                    "failed_verification",
                    "Verification failed and must be visible before action prompts.",
                    card,
                )
            )
        if _is_passed_without_evidence(card):
            top_risks.append(
                _finding(
                    case_id,
                    card["id"],
                    "Error",
                    "passed_verification_without_evidence",
                    "Verification is passed but the card has no evidence refs.",
                    card,
                )
            )
        if _is_done_not_verified(card):
            verification_gaps.append(_card_gap(card, "done but verification is pending"))
            top_actions.append(
                _action(
                    case_id,
                    card["id"],
                    _owner_group(card),
                    "done_not_verified",
                    "Execution is done but verification is still pending.",
                    "Run or record the listed verification method.",
                    card,
                )
            )
        if card["execution_state"] == "waiting":
            top_actions.append(
                _action(
                    case_id,
                    card["id"],
                    _owner_group(card),
                    "waiting_card",
                    "Card is waiting and has a visible expected signal or owner.",
                    _text(card.get("external_dependency", {}).get("expected_signal")) or "Resolve the waiting signal.",
                    card,
                )
            )
        if card["kind"] == "question" and card["owner"] == "user" and card["execution_state"] in {"todo", "waiting"}:
            lanes["question"].append(card["id"])
            top_actions.append(
                _action(
                    case_id,
                    card["id"],
                    "me",
                    "user_owned_question",
                    "A user-owned decision or question is still open.",
                    _first_item(card.get("exit_criteria")) or "Answer the open question.",
                    card,
                )
            )

    for ref in _referenced_card_ids(case_data):
        if ref and ref not in card_by_id:
            validation["errors"].append(f"Missing referenced card: {ref}")
            top_risks.append(
                {
                    "case_id": case_id,
                    "source_ref": f"{case_id}:{ref}",
                    "risk_level": "Error",
                    "matched_rule": "missing_referenced_card",
                    "matched_reason": "A current case field references a missing card file.",
                    "priority": "critical",
                }
            )

    claim_findings = _claim_findings(case_data, evidence_by_id, case_id)
    top_risks.extend(claim_findings["top_risks"])
    trust_gaps.extend(claim_findings["trust_gaps"])
    for finding in claim_findings["trust_gaps"]:
        lanes["trust_gap"].append(finding["source_ref"])
    validation["warnings"].extend(claim_findings["warnings"])

    closeout = _read_closeout(case_dir / "closeout.md")
    closeout_readiness = _closeout_readiness(case_data, lanes, trust_gaps, closeout)
    if closeout_readiness["status"] == "candidate":
        lanes["closeout_candidate"].append(case_id)

    return {
        "case_id": case_id,
        "title": case_data.get("title", case_id),
        "mode": case_data.get("mode", "unknown"),
        "status": case_data.get("status", "unknown"),
        "phase": case_data.get("phase", "unknown"),
        "owner": case_data.get("owner", "unknown"),
        "updated_at": _text(case_data.get("updated_at")),
        "current_conclusion_summary": _text((case_data.get("current_conclusion") or {}).get("summary")),
        "current_focus_card": (case_data.get("current_focus") or {}).get("card_ref"),
        "current_blocker_card": (case_data.get("current_blocker") or {}).get("card_ref"),
        "next_action_card": (case_data.get("next_action") or {}).get("card_ref"),
        "next_action_summary": _text((case_data.get("next_action") or {}).get("summary")),
        "attention_lanes": lanes,
        "risk_counts": _case_risk_counts(top_risks, trust_gaps, verification_gaps),
        "closeout_readiness": closeout_readiness,
        "source_path": str(case_dir / "case.yaml"),
        "cards": cards,
        "claims": case_data.get("claims") or [],
        "evidence": evidence,
        "top_risks": top_risks,
        "top_actions": _dedupe_findings(top_actions),
        "waiting_by_owner": waiting_by_owner,
        "verification_gaps": verification_gaps,
        "trust_gaps": trust_gaps,
        "validation": validation,
    }


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def _read_card(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    frontmatter = _extract_frontmatter(text, path)
    data = yaml.safe_load(frontmatter) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected card frontmatter mapping in {path}")
    data.setdefault("id", path.stem)
    data.setdefault("kind", "unknown")
    data.setdefault("owner", "unknown")
    data.setdefault("execution_state", "unknown")
    data.setdefault("verification_state", "unknown")
    data.setdefault("priority", "medium")
    data.setdefault("external_dependency", {})
    data.setdefault("evidence_refs", [])
    data["source_path"] = str(path)
    return data


def _read_evidence(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    data.setdefault("evidence_id", path.stem)
    data.setdefault("supports", {})
    data.setdefault("limitations", [])
    data["source_path"] = str(path)
    return data


def _extract_frontmatter(text: str, path: Path) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing frontmatter start in {path}")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:index])
    raise ValueError(f"Missing frontmatter end in {path}")


def _read_closeout(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "exists": False,
            "is_draft": False,
            "has_change_section": False,
            "has_trust_section": False,
            "has_learning_section": False,
            "trust_refs": [],
        }
    text = path.read_text(encoding="utf-8")
    return {
        "exists": True,
        "is_draft": "draft" in text.lower() or "historical replay" in text.lower(),
        "has_change_section": "## Change" in text,
        "has_trust_section": "## Trust" in text,
        "has_learning_section": "## Learning" in text,
        "trust_refs": _extract_refs(text),
    }


def _is_card_in_scope(card: Mapping[str, Any], open_refs: set[str], mode: str | None) -> bool:
    scope_status = card.get("scope_status")
    if scope_status in {"in_scope", "historical_only"}:
        return True
    if scope_status in {"out_of_scope", "obsolete"}:
        return False
    if card.get("id") in open_refs:
        return True
    if mode == "historical_replay" and card.get("env") == "historical":
        return True
    return False


def _derive_card_lane(card: Mapping[str, Any]) -> str:
    lanes = _derive_card_lanes(card)
    return lanes[0] if lanes else "none"


def _derive_card_lanes(card: Mapping[str, Any]) -> list[str]:
    lanes: list[str] = []
    execution_state = card.get("execution_state")
    verification_state = card.get("verification_state")
    if execution_state == "blocked" or (
        card.get("kind") == "blocker" and execution_state not in {"done", "cancelled", "obsolete"}
    ):
        lanes.append("blocked")
    if execution_state == "waiting":
        lanes.append("waiting")
    if execution_state == "done" and verification_state == "pending":
        lanes.append("done_not_verified")
    if verification_state == "failed":
        lanes.append("failed_verification")
    return lanes


def _is_failed_verification(card: Mapping[str, Any]) -> bool:
    return card.get("in_current_scope") and card.get("verification_state") == "failed"


def _is_passed_without_evidence(card: Mapping[str, Any]) -> bool:
    return (
        card.get("in_current_scope")
        and card.get("execution_state") == "done"
        and card.get("verification_state") == "passed"
        and not card.get("evidence_refs")
    )


def _is_done_not_verified(card: Mapping[str, Any]) -> bool:
    return (
        card.get("in_current_scope")
        and card.get("execution_state") == "done"
        and card.get("verification_state") == "pending"
    )


def _claim_findings(
    case_data: Mapping[str, Any],
    evidence_by_id: Mapping[str, Mapping[str, Any]],
    case_id: str,
) -> dict[str, list[dict[str, Any]] | list[str]]:
    top_risks: list[dict[str, Any]] = []
    trust_gaps: list[dict[str, Any]] = []
    warnings: list[str] = []
    used_claims = set((case_data.get("current_conclusion") or {}).get("claim_refs") or [])

    for claim in case_data.get("claims") or []:
        claim_id = claim.get("claim_id")
        if not claim_id:
            continue
        evidence_refs = claim.get("evidence_refs") or []
        status = claim.get("status")
        source_ref = f"{case_id}:{claim_id}"
        scope = ((claim.get("claim_scope") or {}).get("truth_environment")) or "unknown"

        if status == "trusted" and not evidence_refs:
            finding = {
                "case_id": case_id,
                "source_ref": source_ref,
                "risk_level": "Error",
                "matched_rule": "trusted_claim_without_evidence",
                "matched_reason": "Trusted claim has no evidence refs.",
                "priority": "high",
                "risk_reasons": ["trusted claim has no evidence refs"],
            }
            top_risks.append(finding)
            trust_gaps.append(finding)

        if claim_id in used_claims and status in {"candidate", "stale"}:
            finding = {
                "case_id": case_id,
                "source_ref": source_ref,
                "risk_level": "Error",
                "matched_rule": f"current_conclusion_uses_{status}_claim",
                "matched_reason": "Current conclusion references a non-trusted claim.",
                "priority": "high",
                "risk_reasons": [f"current conclusion uses {status} claim"],
            }
            top_risks.append(finding)
            trust_gaps.append(finding)

        if claim_id in used_claims and scope == "unknown":
            finding = {
                "case_id": case_id,
                "source_ref": source_ref,
                "risk_level": "Warning",
                "matched_rule": "claim_scope_unknown",
                "matched_reason": "Claim scope is unknown for a claim used by the current conclusion.",
                "priority": "medium",
                "risk_reasons": ["claim scope is unknown"],
            }
            top_risks.append(finding)
            trust_gaps.append(finding)
            warnings.append(f"{source_ref} has unknown claim scope")

        if scope in {"prod", "downstream_actual"} and evidence_refs:
            environments = {
                (evidence_by_id.get(ref) or {}).get("environment", "unknown")
                for ref in evidence_refs
            }
            if environments and environments <= {"test", "historical", "plan", "analysis"}:
                finding = {
                    "case_id": case_id,
                    "source_ref": source_ref,
                    "risk_level": "Error",
                    "matched_rule": "current_truth_supported_only_by_limited_evidence",
                    "matched_reason": "Prod/downstream claim is backed only by test or historical evidence.",
                    "priority": "high",
                    "risk_reasons": ["prod/downstream claim has limited evidence only"],
                }
                top_risks.append(finding)
                trust_gaps.append(finding)

    return {"top_risks": top_risks, "trust_gaps": trust_gaps, "warnings": warnings}


def _referenced_card_ids(case_data: Mapping[str, Any]) -> set[str]:
    refs = set(case_data.get("open_card_refs") or [])
    for key in ["current_focus", "current_blocker", "next_action"]:
        ref = (case_data.get(key) or {}).get("card_ref")
        if ref:
            refs.add(ref)
    return refs


def _closeout_readiness(
    case_data: Mapping[str, Any],
    lanes: Mapping[str, list[str]],
    trust_gaps: list[Mapping[str, Any]],
    closeout: Mapping[str, Any],
) -> dict[str, Any]:
    blockers = bool(lanes.get("blocked"))
    failed = bool(lanes.get("failed_verification"))
    trust_gap = bool(trust_gaps)
    has_trust = closeout.get("has_trust_section") and closeout.get("trust_refs")
    if blockers or failed or trust_gap or not has_trust:
        return {
            "status": "not_ready",
            "reasons": _compact_list(
                [
                    "open blockers" if blockers else "",
                    "failed verification" if failed else "",
                    "trust gaps" if trust_gap else "",
                    "missing evidence-backed Trust section" if not has_trust else "",
                ]
            ),
        }
    if case_data.get("mode") == "historical_replay":
        return {"status": "candidate", "reasons": ["historical replay requires explicit final review"]}
    return {"status": "candidate", "reasons": ["structurally ready for closeout review"]}


def _case_risk_counts(
    top_risks: list[Mapping[str, Any]],
    trust_gaps: list[Mapping[str, Any]],
    verification_gaps: list[Mapping[str, Any]],
) -> dict[str, int]:
    return {
        "errors": sum(1 for item in top_risks if item.get("risk_level") == "Error"),
        "warnings": sum(1 for item in top_risks if item.get("risk_level") == "Warning"),
        "trust_gaps": len(trust_gaps),
        "verification_gaps": len(verification_gaps),
    }


def _build_health(cases: list[Mapping[str, Any]]) -> dict[str, int]:
    cards = [card for case in cases for card in case["cards"]]
    trust_gaps = [gap for case in cases for gap in case["trust_gaps"]]
    evidence = [item for case in cases for item in case["evidence"]]
    validation_errors = sum(len(case["validation"]["errors"]) for case in cases)
    validation_warnings = sum(len(case["validation"]["warnings"]) for case in cases)
    validation_info = sum(len(case["validation"]["info"]) for case in cases)
    return {
        "case_count": len(cases),
        "active_case_count": sum(1 for case in cases if case.get("status") == "active"),
        "stale_waiting_count": sum(1 for card in cards if card.get("execution_state") == "waiting"),
        "unverified_done_count": sum(1 for card in cards if _is_done_not_verified(card)),
        "failed_verification_count": sum(1 for card in cards if _is_failed_verification(card)),
        "trusted_claim_without_evidence_count": sum(
            1
            for gap in trust_gaps
            if gap.get("matched_rule") == "trusted_claim_without_evidence"
        ),
        "candidate_claim_used_by_next_action_count": 0,
        "historical_or_test_evidence_for_current_truth_count": sum(
            1
            for gap in trust_gaps
            if gap.get("matched_rule") == "current_truth_supported_only_by_limited_evidence"
        ),
        "evidence_without_refs_count": sum(1 for item in evidence if not _evidence_support_refs(item)),
        "closeout_candidate_count": sum(
            1 for case in cases if case["closeout_readiness"]["status"] == "candidate"
        ),
        "validation_error_count": validation_errors,
        "validation_warning_count": validation_warnings,
        "validation_info_count": validation_info,
    }


def _finding(
    case_id: str,
    card_id: str,
    risk_level: str,
    matched_rule: str,
    matched_reason: str,
    card: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "card_id": card_id,
        "source_ref": f"{case_id}:{card_id}",
        "risk_level": risk_level,
        "matched_rule": matched_rule,
        "matched_reason": matched_reason,
        "priority": card.get("priority", "medium"),
        "title": _text(card.get("title")),
    }


def _action(
    case_id: str,
    card_id: str,
    owner_group: str,
    matched_rule: str,
    matched_reason: str,
    next_action: str,
    card: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "card_id": card_id,
        "source_ref": f"{case_id}:{card_id}",
        "owner_group": owner_group,
        "matched_rule": matched_rule,
        "matched_reason": matched_reason,
        "next_action": next_action,
        "priority": card.get("priority", "medium"),
        "title": _text(card.get("title")),
    }


def _card_gap(card: Mapping[str, Any], reason: str) -> dict[str, Any]:
    return {
        "case_id": card["case_id"],
        "card_id": card["id"],
        "title": _text(card.get("title")),
        "execution_state": card.get("execution_state"),
        "verification_state": card.get("verification_state"),
        "risk_reasons": reason,
        "source_path": card.get("source_path"),
    }


def _card_action_summary(card: Mapping[str, Any], case_id: str) -> dict[str, Any]:
    dependency = card.get("external_dependency") or {}
    return {
        "case_id": case_id,
        "card_id": card.get("id"),
        "title": _text(card.get("title")),
        "owner_group": _owner_group(card),
        "waiting_on": _text(dependency.get("waiting_on")),
        "expected_signal": _text(dependency.get("expected_signal")),
        "blocked_since": _text(dependency.get("blocked_since")),
        "next_touch_at": _text(dependency.get("next_touch_at")),
        "risk_reasons": "waiting for external signal",
        "source_path": card.get("source_path"),
    }


def _owner_group(card: Mapping[str, Any]) -> str:
    owner = _text(card.get("owner")).lower()
    waiting_on = _text((card.get("external_dependency") or {}).get("waiting_on")).lower()
    combined = f"{owner} {waiting_on}"
    if any(token in combined for token in ["user", "me", "human", "鐢ㄦ埛"]):
        return "me"
    if any(token in combined for token in ["codex", "agent"]):
        return "Codex"
    if any(token in combined for token in ["approver", "approval", "审批"]):
        return "approver"
    if any(token in combined for token in ["platform", "horae", "oracle"]):
        return "platform"
    if "partner" in combined:
        return "partner"
    return "unknown"


def _risk_sort_key(item: Mapping[str, Any]) -> tuple[int, int, str]:
    level_rank = {"Error": 0, "Warning": 1, "Info": 2}.get(item.get("risk_level"), 3)
    return (level_rank, PRIORITY_RANK.get(str(item.get("priority")), 9), str(item.get("source_ref")))


def _action_sort_key(item: Mapping[str, Any]) -> tuple[int, str]:
    owner_rank = {"me": 0, "Codex": 1, "partner": 2, "approver": 3, "platform": 4}.get(
        item.get("owner_group"), 5
    )
    return (owner_rank, str(item.get("source_ref")))


def _dedupe_findings(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = (item.get("source_ref", ""), item.get("matched_rule", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def _evidence_support_refs(evidence: Mapping[str, Any]) -> list[str]:
    supports = evidence.get("supports") or {}
    return list(supports.get("claim_refs") or []) + list(supports.get("card_refs") or [])


def _extract_refs(text: str) -> list[str]:
    refs: list[str] = []
    for token in text.replace("`", " ").replace(",", " ").replace(";", " ").split():
        stripped = token.strip("[]().:-")
        if len(stripped) >= 4 and stripped[0] in {"C", "T", "B", "Q", "D"} and "-" in stripped:
            refs.append(stripped)
        elif stripped.startswith("EV-"):
            refs.append(stripped)
    return refs


def _render_health(health: Mapping[str, int]) -> str:
    labels = [
        ("case_count", "Cases"),
        ("active_case_count", "Active"),
        ("failed_verification_count", "Failed Verification"),
        ("unverified_done_count", "Done Not Verified"),
        ("trusted_claim_without_evidence_count", "Trusted Claim Gaps"),
        ("evidence_without_refs_count", "Unlinked Evidence"),
        ("closeout_candidate_count", "Closeout Candidates"),
    ]
    return '<div class="health">' + "".join(
        f'<div class="metric"><strong>{health[key]}</strong><span>{escape(label)}</span></div>'
        for key, label in labels
    ) + "</div>"


def _render_rows(items: list[Mapping[str, Any]], fields: list[str], empty: str) -> str:
    if not items:
        return f"<p>{escape(empty)}</p>"
    header = "".join(f"<th>{escape(field.replace('_', ' ').title())}</th>" for field in fields)
    rows = []
    for item in items:
        cells = "".join(f"<td>{_format_cell(item.get(field))}</td>" for field in fields)
        rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def _render_waiting_group(group: str, items: list[Mapping[str, Any]]) -> str:
    rows = _render_rows(
        items,
        ["case_id", "card_id", "title", "waiting_on", "expected_signal", "next_touch_at"],
        empty="No waiting cards.",
    )
    return f"<h3>{escape(group)}</h3>{rows}"


def _render_case_summary(case: Mapping[str, Any]) -> str:
    lanes = ", ".join(
        f"{key}: {len(values)}" for key, values in case["attention_lanes"].items() if values
    )
    mode_class = "warning" if case.get("mode") == "historical_replay" else "badge"
    return f"""
<article class="case-summary">
  <h3>{escape(str(case["case_id"]))}</h3>
  <p>{escape(_text(case.get("title")))}</p>
  <p><span class="{mode_class}">{escape(_text(case.get("mode")))}</span>
     <span class="badge">{escape(_text(case.get("phase")))}</span>
     <span class="badge">{escape(_text(case.get("status")))}</span></p>
  <p>Focus: <code>{escape(_text(case.get("current_focus_card")))}</code></p>
  <p>Blocker: <code>{escape(_text(case.get("current_blocker_card")))}</code></p>
  <p>Next: {escape(_text(case.get("next_action_summary")))}</p>
  <p>Lanes: {escape(lanes or "none")}</p>
  <p>Source: <code>{escape(_text(case.get("source_path")))}</code></p>
</article>
"""


def _format_cell(value: Any) -> str:
    if isinstance(value, list):
        return escape(", ".join(_text(item) for item in value))
    if str(value) in {"Error", "Warning"}:
        cls = "error" if value == "Error" else "warning"
        return f'<span class="{cls}">{escape(str(value))}</span>'
    return escape(_text(value))


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _first_item(value: Any) -> str:
    if isinstance(value, list) and value:
        return _text(value[0])
    return _text(value)


def _compact_list(values: list[str]) -> list[str]:
    return [value for value in values if value]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a read-only Case dashboard.")
    parser.add_argument("--source-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("tmp/case-dashboard/index.html"))
    args = parser.parse_args(argv)

    write_dashboard(args.source_root, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

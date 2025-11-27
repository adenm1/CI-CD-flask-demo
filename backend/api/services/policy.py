"""Simple rule-based policy evaluation."""
from datetime import datetime
from typing import Dict, List, Tuple

from backend.api.models import PolicyDecision
from backend.utils.db import get_session


def evaluate_action(actor: str, action: str, context: Dict) -> Tuple[str, List[str], Dict]:
    """Return (decision, rules, evidence). Decisions: allow, deny, challenge."""
    rules_triggered: List[str] = []
    evidence: Dict = {}
    decision = "allow"

    hour = datetime.utcnow().hour
    if hour < 6 or hour > 22:
        rules_triggered.append("after_hours")
        decision = "challenge"
        evidence["hour"] = hour

    risk_score = context.get("risk_score", 0)
    evidence["risk_score"] = risk_score
    if risk_score >= 70:
        rules_triggered.append("high_risk_score")
        decision = "deny"
    elif risk_score >= 40 and decision != "deny":
        rules_triggered.append("medium_risk_score")
        decision = "challenge"

    return decision, rules_triggered, evidence


def persist_decision(actor: str, action: str, decision: str, rules: List[str], evidence: Dict) -> None:
    """Store policy decision for auditability."""
    session = get_session()
    record = PolicyDecision(
        actor=actor,
        action=action,
        decision=decision,
        rules=",".join(rules) if rules else "",
        evidence=str(evidence) if evidence else "",
    )
    session.add(record)
    session.commit()

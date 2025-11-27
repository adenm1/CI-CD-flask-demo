"""Risk scoring and challenge handling."""
from datetime import datetime, timezone
import secrets
import hashlib
from typing import Optional, Tuple

import pyotp

from backend.api.models import AdminUser, AuthChallenge
from backend.utils.db import get_session


def calculate_risk(remote_addr: Optional[str], failures: int = 0) -> int:
    """Basic risk: more failures and off-hours raise score."""
    score = 10
    hour = datetime.utcnow().hour
    if hour < 6 or hour > 22:
        # Off-hours increase risk but should not automatically force MFA
        score += 20
    if failures >= 3:
        score += 40
    if failures >= 5:
        score += 60
    if remote_addr and remote_addr.startswith("10."):
        score -= 10  # internal network slightly safer
    return max(0, min(score, 100))


def issue_totp_challenge(username: str, risk_score: int) -> AuthChallenge:
    """Create a TOTP challenge record (code is validated via authenticator)."""
    session = get_session()
    # TOTP codes are verified dynamically; store placeholder hash for audit
    dummy_code = secrets.token_hex(8)
    code_hash = hashlib.sha256(dummy_code.encode()).hexdigest()
    challenge = AuthChallenge(
        admin_username=username,
        method="totp",
        code_hash=code_hash,
        risk_score=risk_score,
        status="pending",
    )
    session.add(challenge)
    session.commit()
    session.refresh(challenge)
    return challenge


def verify_totp(admin: AdminUser, code: str) -> bool:
    """Verify a TOTP code for the admin."""
    if not admin.totp_secret:
        return False
    totp = pyotp.TOTP(admin.totp_secret)
    return totp.verify(code, valid_window=1)

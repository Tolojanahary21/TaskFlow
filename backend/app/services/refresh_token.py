from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..core.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    get_refresh_token_expiration,
    decode_token
)

from ..models.refresh_token import RefreshToken


def save_refresh_token(db: Session, user_id: int):

    expires_at = get_refresh_token_expiration()

    token = create_refresh_token({
        "sub": str(user_id)
    })

    token_hash = hash_refresh_token(token)

    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        revoked=False
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return token


def verify_refresh_token(db: Session, token: str):

    payload = decode_token(token)

    if not payload:
        return None

    if payload.get("type") != "refresh":
        return None

    user_id = payload.get("sub")

    if not user_id:
        return None

    token_hash = hash_refresh_token(token)

    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.user_id == int(user_id)
        )
        .first()
    )

    if not refresh_token:
        return None

    if refresh_token.revoked:
        return None

    if refresh_token.expires_at <= datetime.now():
        return None

    return refresh_token
def refresh_access_token(db: Session, token: str):

    refresh_token = verify_refresh_token(db, token)

    if not refresh_token:
        return None

    access_token = create_access_token({
        "sub": str(refresh_token.user_id)
    })

    return access_token
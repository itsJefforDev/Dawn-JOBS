from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings


# ============================================================
# PASSWORD HASHING
# ============================================================

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña.
    """

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verifica una contraseña contra su hash.
    """

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# JWT
# ============================================================

def create_access_token(
    user_id: int,
    email: str
) -> str:
    """
    Genera un JWT para el usuario autenticado.
    """

    now = datetime.now(timezone.utc)

    expires = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expires
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(
    token: str
) -> dict | None:
    """
    Decodifica y valida un JWT.

    Retorna:
        dict: payload si el token es válido.
        None: si el token es inválido o expiró.
    """

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:

        return None
"""
app/core/dependencies.py

Dependencias relacionadas con la autenticación.

Responsabilidades:
    - Extraer el JWT desde el header Authorization.
    - Validar el JWT.
    - Obtener el usuario autenticado.
    - Proporcionar current_user a los endpoints protegidos.

Las APIs privadas utilizarán:

    Depends(get_current_user)

Por seguridad, el frontend nunca enviará user_id
para identificar al usuario.
"""

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


# ============================================================
# HTTP BEARER
# ============================================================

"""
HTTPBearer indica que nuestra API utiliza:

    Authorization: Bearer <JWT>

Esto es diferente de OAuth2PasswordBearer.

No estamos implementando el flujo OAuth2 Password.
Nuestro login es un endpoint JSON que genera un JWT.
"""

security = HTTPBearer()


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Obtiene el usuario autenticado desde el JWT.

    Flujo:

        Authorization Header
                ↓
        Bearer <JWT>
                ↓
        decode_access_token()
                ↓
        user_id
                ↓
        Database
                ↓
        User
    """

    # --------------------------------------------------------
    # Extraer token
    # --------------------------------------------------------

    token = credentials.credentials

    # --------------------------------------------------------
    # Decodificar JWT
    # --------------------------------------------------------

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # --------------------------------------------------------
    # Obtener ID del usuario
    # --------------------------------------------------------

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # --------------------------------------------------------
    # Buscar usuario
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # --------------------------------------------------------
    # Usuario autenticado
    # --------------------------------------------------------

    return user
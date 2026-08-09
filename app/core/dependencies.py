"""
app/core/dependencies.py

Dependencias utilizadas por FastAPI para proteger los endpoints
que requieren autenticación.

Responsabilidades:

    - Obtener el token JWT enviado por el cliente.
    - Validar el token.
    - Obtener el ID del usuario.
    - Buscar al usuario en la base de datos.
    - Retornar el usuario autenticado.

Todas las APIs privadas del sistema deberán utilizar:

    Depends(get_current_user)

De esta manera NO necesitamos recibir user_id desde el frontend.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


# ============================================================
# CONFIGURACIÓN DEL TOKEN
# ============================================================

"""
OAuth2PasswordBearer le indica a FastAPI que el token JWT será
enviado mediante:

    Authorization: Bearer <TOKEN>

El parámetro tokenUrl indica dónde se realiza el login.

IMPORTANTE:

Esto NO realiza el login.

Únicamente permite que FastAPI extraiga el token de las
peticiones protegidas.
"""

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ============================================================
# USUARIO AUTENTICADO
# ============================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Obtiene el usuario actualmente autenticado.

    Flujo:

        Request
            ↓
        Authorization: Bearer TOKEN
            ↓
        OAuth2PasswordBearer
            ↓
        JWT
            ↓
        decode_access_token()
            ↓
        user_id
            ↓
        Base de datos
            ↓
        User
    """

    # --------------------------------------------------------
    # Decodificar el JWT
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
    # Obtener el user_id desde el JWT
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
    # Buscar el usuario en la base de datos
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
    # Retornar usuario autenticado
    # --------------------------------------------------------

    return user
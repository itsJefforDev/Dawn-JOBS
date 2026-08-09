"""
app/core/security.py

Módulo central de seguridad de la aplicación.

Responsabilidades:
    - Generar hashes seguros para las contraseñas.
    - Verificar contraseñas.
    - Crear tokens JWT.
    - Decodificar y validar tokens JWT.

IMPORTANTE:
    Este archivo NO debe contener lógica de negocio.
    La identificación del usuario autenticado se realiza
    posteriormente mediante `get_current_user()` en:

        app/api/dependencies.py
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings


# ============================================================
# PASSWORD HASHING
# ============================================================

"""
`pwdlib` utiliza algoritmos modernos de hashing de contraseñas.

En lugar de guardar la contraseña original:

    password = "MiPassword123"

guardamos únicamente un hash:

    $argon2id$...

De esta manera, aunque alguien obtuviera acceso a la base
de datos, no tendría acceso directo a las contraseñas.
"""

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de una contraseña.

    Args:
        password:
            Contraseña original proporcionada por el usuario.

    Returns:
        str:
            Hash de la contraseña.

    Ejemplo:

        password = "Password123"

        hash_password(password)

        -> "$argon2id$..."
    """

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verifica si una contraseña coincide con su hash.

    Args:
        plain_password:
            Contraseña enviada durante el login.

        hashed_password:
            Hash almacenado en la base de datos.

    Returns:
        bool:
            True si la contraseña es correcta.
            False si no coincide.
    """

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# JWT
# ============================================================

"""
Los JWT permiten identificar al usuario después del login.

El flujo es:

    LOGIN
      ↓
    Usuario + contraseña
      ↓
    Verificación
      ↓
    JWT
      ↓
    Frontend almacena token
      ↓
    Peticiones posteriores
      ↓
    Authorization: Bearer <token>
      ↓
    get_current_user()
      ↓
    Usuario autenticado
"""


def create_access_token(
    user_id: int,
    email: str
) -> str:
    """
    Genera un JWT para un usuario autenticado.

    El token contiene únicamente información necesaria
    para identificar al usuario.

    Args:
        user_id:
            ID del usuario en la base de datos.

        email:
            Email del usuario.

    Returns:
        str:
            Token JWT firmado.
    """

    # Tiempo actual en UTC.
    now = datetime.now(timezone.utc)

    # Tiempo de expiración configurado en la aplicación.
    expires = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Información que almacenaremos dentro del JWT.
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expires
    }

    # Firmamos el token utilizando la SECRET_KEY.
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict | None:
    """
    Decodifica y valida un JWT.

    Args:
        token:
            Token JWT recibido desde el frontend.

    Returns:
        dict | None:
            Payload del token si es válido.
            None si el token es inválido o está expirado.

    Esta función NO busca al usuario en la base de datos.

    Esa responsabilidad pertenece a:

        get_current_user()
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
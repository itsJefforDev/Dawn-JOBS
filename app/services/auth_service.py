from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreate

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


# ============================================================
# REGISTRO DE USUARIO
# ============================================================

def create_user(db: Session, user_data: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.

    Flujo:
        1. Verifica que el email no esté registrado.
        2. Hashea la contraseña.
        3. Crea el usuario.
        4. Guarda el usuario en la base de datos.
        5. Devuelve el usuario creado.

    IMPORTANTE:
        La contraseña NUNCA se almacena directamente.
        Solamente se almacena su hash.
    """

    # --------------------------------------------------------
    # Verificar si el email ya existe
    # --------------------------------------------------------

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        return None

    # --------------------------------------------------------
    # Crear usuario
    # --------------------------------------------------------

    new_user = User(
        name=user_data.name,
        email=user_data.email,

        # La contraseña se transforma en un hash
        password_hash=hash_password(user_data.password_hash)
    )

    # --------------------------------------------------------
    # Guardar en la base de datos
    # --------------------------------------------------------

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ============================================================
# LOGIN
# ============================================================

def login_user(db: Session, email: str, password: str):
    """
    Autentica un usuario.

    Flujo:

        1. Busca el usuario mediante su email.
        2. Verifica la contraseña.
        3. Genera un JWT.
        4. Devuelve el token y datos básicos del usuario.

    El JWT será utilizado posteriormente por las APIs
    protegidas para identificar al usuario autenticado.
    """

    # --------------------------------------------------------
    # Buscar usuario
    # --------------------------------------------------------

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    # --------------------------------------------------------
    # Verificar contraseña
    # --------------------------------------------------------

    if not verify_password(password, user.password_hash):
        return None

    # --------------------------------------------------------
    # Crear JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    # --------------------------------------------------------
    # Respuesta del login
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }
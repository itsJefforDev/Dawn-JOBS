"""
Servicio de autenticación.

Este módulo contiene la lógica de negocio relacionada con:

    - Registro de usuarios.
    - Autenticación de usuarios.
    - Generación de tokens JWT.

Responsabilidades:
    - Consultar usuarios en la base de datos.
    - Validar credenciales.
    - Generar hashes de contraseñas.
    - Generar tokens de acceso.

Este módulo NO se encarga de:
    - Recibir peticiones HTTP.
    - Definir rutas.
    - Extraer el JWT del request.

La lógica HTTP pertenece a:
    app/api/routes/auth.py

La validación del usuario autenticado pertenece a:
    app/core/dependencies.py
"""

from fastapi import HTTPException, status
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

def create_user(
    db: Session,
    user_data: UserCreate
):
    """
    Crea un nuevo usuario.

    Flujo:

        1. Busca si el email ya está registrado.
        2. Si existe, devuelve 409 Conflict.
        3. Hashea la contraseña.
        4. Crea el usuario.
        5. Guarda el usuario en PostgreSQL.
        6. Devuelve el usuario creado.

    Parámetros
    ----------
    db:
        Sesión activa de SQLAlchemy.

    user_data:
        Datos enviados por el usuario durante el registro.

    Returns
    -------
    User:
        Usuario creado.

    Raises
    ------
    HTTPException:
        409 si el email ya está registrado.
    """

    # --------------------------------------------------------
    # Verificar email existente
    # --------------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # --------------------------------------------------------
    # Crear usuario
    # --------------------------------------------------------

    new_user = User(
        name=user_data.name,
        email=user_data.email,

        # Nunca almacenamos la contraseña original.
        # Se almacena únicamente el hash.
        password_hash=hash_password(
            user_data.password
        )
    )

    # --------------------------------------------------------
    # Persistir usuario
    # --------------------------------------------------------

    db.add(new_user)
    db.commit()

    # Recargar el objeto para obtener, por ejemplo,
    # el ID generado por PostgreSQL.
    db.refresh(new_user)

    return new_user


# ============================================================
# LOGIN
# ============================================================

def login_user(
    db: Session,
    email: str,
    password: str
):
    """
    Autentica un usuario y genera un JWT.

    Flujo:

        email + password
                ↓
        Buscar usuario
                ↓
        Verificar contraseña
                ↓
        Generar JWT
                ↓
        Devolver token

    Parámetros
    ----------
    db:
        Sesión activa de SQLAlchemy.

    email:
        Email enviado durante el login.

    password:
        Contraseña en texto plano enviada por el usuario.

    Returns
    -------
    dict | None:
        Información del token si las credenciales son correctas.
        None si las credenciales no son válidas.

    Nota de seguridad:
        No diferenciamos entre "usuario no existe" y
        "contraseña incorrecta" para evitar revelar qué
        emails están registrados.
    """

    # --------------------------------------------------------
    # Buscar usuario
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    # --------------------------------------------------------
    # Verificar contraseña
    # --------------------------------------------------------

    password_valid = verify_password(
        password,
        user.password_hash
    )

    if not password_valid:
        return None

    # --------------------------------------------------------
    # Generar JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        user_id=user.id,
        email=user.email
    )

    # --------------------------------------------------------
    # Respuesta
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer",

        # Información básica del usuario.
        # Nunca incluimos password_hash.
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }
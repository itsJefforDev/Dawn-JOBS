"""
Dependencias relacionadas con autenticación.

Este módulo permite obtener automáticamente el usuario
actual autenticado mediante el JWT enviado en el Header.

Todas las APIs privadas utilizarán estas dependencias
para evitar recibir el user_id manualmente.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
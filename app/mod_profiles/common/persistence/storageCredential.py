# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from app.mod_profiles.models.StorageCredential import StorageCredential
from app.mod_profiles.models.User import User

def get_by_user(user):
    if not isinstance(user, User):
        raise ValueError("El perfil especificado es incorrecto.")
    storage_credentials = StorageCredential.query.all()
    user_storage_credentials = []
    for storage_credential in storage_credentials:
        if storage_credential.id == user.id:
            user_storage_credentials.append(storage_credential)
    return user_storage_credentials


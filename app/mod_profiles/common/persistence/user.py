# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from app.mod_profiles.models import User


def update(user, username=None, email=None, password=None, profile_id=None):
    """Actualiza la información de una instancia de usuario, y la retorna.

    Actualiza los atributos y relaciones de una instancia de usuario, en base a
    los parámetros recibidos. Retorna el usuario actualizado.

    :param user: Usuario a ser actualizado.
    :param username: Nombre de usuario.
    :param email: Dirección de correo electrónico del usuario.
    :param password: Contraseña del usuario, en texto plano.
    :param profile_id: Identificador único del perfil asociado al usuario.
    :return: Usuario actualizado.
    """

    # Valida que el usuario sea correcto.
    if not isinstance(user, User):
        raise ValueError("El usuario especificado es incorrecto.")

    # Actualiza el nombre de usuario, en caso de que haya sido modificado.
    if (username is not None and
          user.username != username):
        user.username = username
    # Actualiza la dirección de correo electrónico, en caso de que haya
    # sido modificado.
    if (email is not None and
          user.email != email):
        user.email = email
    # Actualiza la contraseña, en caso de que haya sido modificado.
    if (password is not None and
          len(password) > 0 and
          not user.verify_password(password)):
        user.hash_password(password)
    # Actualiza el perfil asociado, en caso de que haya sido modificado.
    if (profile_id is not None and
          user.profile_id != profile_id):
        user.profile_id = profile_id

    db.session.commit()

    return user

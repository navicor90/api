# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from app.mod_profiles.models import Profile


def update(profile, first_name=None, last_name=None, birthday=None, gender_id=None):
    """Actualiza la información de una instancia de perfil, y la retorna.

    Actualiza los atributos y relaciones de una instancia de perfil, en base a
    los parámetros recibidos. Retorna el perfil actualizado.

    :param profile: Perfil a ser actualizado.
    :param first_name: Nombre de la persona.
    :param last_name: Apellido de la persona.
    :param birthday: Fecha de nacimiento de la persona, en formato ISO 8601.
    :param gender_id: Identificador único del género asociado al perfil.
    :return: Perfil actualizado.
    """

    # Valida que el perfil sea correcto.
    if not isinstance(profile, Profile):
        raise ValueError("El perfil especificado es incorrecto.")

    # Actualiza el apellido, en caso de que haya sido modificado.
    if (last_name is not None and
          profile.last_name != last_name):
        profile.last_name = last_name
    # Actualiza el nombre, en caso de que haya sido modificado.
    if (first_name is not None and
          profile.first_name != first_name):
        profile.first_name = first_name
    # Actualiza la fecha de nacimiento, en caso de que haya sido
    # modificada.
    if (birthday is not None and
          profile.birthday != birthday):
        profile.birthday = birthday
    # Actualiza el genero, en caso de que haya sido modificado.
    if (gender_id is not None and
          profile.gender_id != gender_id):
        profile.gender_id = gender_id

    db.session.commit()

    return profile

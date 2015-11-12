# -*- coding: utf-8 -*-

from hashlib import md5
from urllib import urlencode

from app.mod_profiles.models import User


def get_gravatar_url(user, default_image, size):
    # Valida que el usuario sea correcto.
    if not isinstance(user, User):
        raise ValueError("El usuario especificado es incorrecto.")

    # Reemplaza los valores de los parámetros, en caso de que sean nulos.
    default_image = default_image or 'identicon'
    size = size or 80

    # Configura la dirección URL base de Gravatar.
    base_url = 'http://www.gravatar.com/avatar/'
    # Calcula la suma MD5 del correo electrónico del usuario.
    user_email_hash = md5(user.email.lower().strip()).hexdigest()

    # Construye la URL de Gravatar para la imagen de perfil del usuario.
    gravatar_url = base_url + user_email_hash + '.jpg?'
    gravatar_url += urlencode({
        'd': default_image,
        's': str(size),
    })

    return gravatar_url

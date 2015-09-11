# coding=utf-8

from flask import g
from flask.ext.httpauth import HTTPBasicAuth
from app.mod_profiles.models.User import User

# Manejo de autenticación HTTP.
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # Prueba la autenticación mediante token.
    user = User.verify_auth_token(username_or_token)
    if not user:
        # Prueba la autenticación mediante usuario y contraseña.
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
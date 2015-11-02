# -*- coding: utf-8 -*-

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from Crypto.PublicKey import RSA

from app.config import Config
from app.mod_shared.models.db import db


class User(db.Model):
    # Attributes
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(32), unique=True, index=True)
    email           = db.Column(db.String(64), unique=True)
    password_hash   = db.Column(db.String(128))
    rsa_private_key = db.Column(db.Text)
    rsa_public_key  = db.Column(db.Text)
    # Foreign keys
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    profile = db.relationship('Profile',
                              backref=db.backref('user', lazy='dynamic'))

    def __init__(self, username, email, password, profile_id):
        self.username = username
        self.email = email
        self.hash_password(password)
        self.profile_id = profile_id
        self.create_rsa_keys(2048)

    def __repr__(self):
        return '<User: %r>' % (self.username)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Token válido, pero expirado.
            return None
        except BadSignature:
            # Token inválido.
            return None
        user = User.query.get(data['id'])
        return user

    def create_rsa_keys(self, key_size=2048):
        # Verifica que el usuario no tenga una clave privada asociada.
        if (self.rsa_private_key is None or
                self.rsa_private_key == ''):
            # Crea el par de claves RSA.
            private_key = RSA.generate(key_size)
            public_key = private_key.publickey()
            # Asocia las claves al usuario.
            self.rsa_private_key = private_key.exportKey()
            self.rsa_public_key = public_key.exportKey()
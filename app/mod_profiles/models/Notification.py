# -*- coding: utf-8 -*-

from datetime import datetime

from app.mod_shared.models.db import db


class Notification(db.Model):
    # Attributes
    id               = db.Column(db.Integer, primary_key=True)
    created_datetime = db.Column(db.DateTime)
    read_datetime    = db.Column(db.DateTime)
    type             = db.Column(db.String(50))
    # Foreign keys
    notification_owner_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    notification_owner = db.relationship('Profile',
                                         backref=db.backref('notifications', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'notification',
        'polymorphic_on': type
    }

    def __init__(self, notification_owner_id):
        self.created_datetime      = datetime.utcnow()
        self.read_datetime         = None
        self.notification_owner_id = notification_owner_id

    def set_as_read(self):
        self.read_datetime = datetime.utcnow()

    def get_title(self):
        raise NotImplementedError(u'Método no implementado.')

    def get_description(self):
        raise NotImplementedError(u'Método no implementado.')

    def get_detail_object_type(self):
        raise NotImplementedError(u'Método no implementado.')

    def get_detail_object_id(self):
        raise NotImplementedError(u'Método no implementado.')

    def get_notification_type(self):
        raise NotImplementedError(u'Método no implementado.')

    def __repr__(self):
        return '<Notification: %r>' % self.id

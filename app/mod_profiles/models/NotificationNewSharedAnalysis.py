# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from .Notification import Notification


class NotificationNewSharedAnalysis(Notification):
    # Attributes
    id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    # Foreign keys
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    profile_id    = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    permission = db.relationship('Permission',
                                 backref=db.backref('notifications',
                                                    lazy='dynamic',
                                                    cascade='all, delete-orphan',
                                                    )
                                 )
    profile    = db.relationship('Profile')

    __mapper_args__ = {
        'polymorphic_identity': 'notificationNewSharedAnalysis',
    }

    def __init__(self, notification_owner_id, permission_id, profile_id):
        Notification.__init__(self, notification_owner_id)
        self.permission_id = permission_id
        self.profile_id    = profile_id

    def get_title(self):
        return u'¡Han compartido un análisis contigo!'

    def get_description(self):
        description = u"%s ha compartido el análisis \"%s\" contigo." % (
            self.profile.first_name + " " + self.profile.last_name,
            self.permission.analysis.description,
        )
        return description

    @staticmethod
    def get_detail_object_type():
        return 'analysis'

    def get_detail_object_id(self):
        return self.permission.analysis.id

    def __repr__(self):
        return '<NotificationNewSharedAnalysis: %r>' % self.id

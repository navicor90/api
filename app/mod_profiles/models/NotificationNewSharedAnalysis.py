# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from .Notification import Notification


class NotificationNewSharedAnalysis(Notification):
    # Attributes
    id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    # Foreign keys
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
    # Relationships
    permission = db.relationship('Permission',
                                 backref=db.backref('notifications',
                                                    lazy='dynamic',
                                                    cascade='all, delete-orphan',
                                                    )
                                 )

    __mapper_args__ = {
        'polymorphic_identity': 'notificationNewSharedAnalysis',
    }

    def __init__(self, notification_owner_id, notification_author_id, permission_id):
        Notification.__init__(self, notification_owner_id, notification_author_id)
        self.permission_id = permission_id

    def get_title(self):
        author = self.notification_author
        title = u'¡%s ha compartido un análisis contigo!' % (
            author.first_name + ' ' + author.last_name,
        )
        return title

    def get_description(self):
        author = self.notification_author
        description = u'%s ha compartido el análisis "%s" contigo.' % (
            author.first_name + ' ' + author.last_name,
            self.permission.analysis.description,
        )
        return description

    @staticmethod
    def get_detail_object_type():
        return 'analysis'

    def get_detail_object_id(self):
        return self.permission.analysis.id

    @staticmethod
    def get_notification_type():
        return 'event'

    def __repr__(self):
        return '<NotificationNewSharedAnalysis: %r>' % self.id

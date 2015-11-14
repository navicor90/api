# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from .Notification import Notification


class NotificationNewGroupMembership(Notification):
    # Attributes
    id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    # Foreign keys
    group_membership_id = db.Column(db.Integer, db.ForeignKey('group_membership.id'))
    # Relationships
    group_membership = db.relationship('GroupMembership',
                                       backref=db.backref('notifications',
                                                          lazy='dynamic',
                                                          cascade='all, delete-orphan',
                                                          )
                                       )

    __mapper_args__ = {
        'polymorphic_identity': 'notificationNewGroupMembership',
    }

    def __init__(self, notification_owner_id, notification_author_id, group_membership_id):
        Notification.__init__(self, notification_owner_id, notification_author_id)
        self.group_membership_id = group_membership_id

    def get_title(self):
        author = self.notification_author
        title = u'¡%s te ha agregado a un grupo!' % (
            author.first_name + ' ' + author.last_name,
        )
        return title

    def get_description(self):
        author = self.notification_author
        description = u'%s te ha agregado al grupo "%s".' % (
            author.first_name + ' ' + author.last_name,
            self.group_membership.group.name,
        )
        return description

    @staticmethod
    def get_detail_object_type():
        return 'group'

    def get_detail_object_id(self):
        return self.group_membership.group.id

    @staticmethod
    def get_notification_type():
        return 'event'

    def __repr__(self):
        return '<NotificationNewGroupMembership: %r>' % self.id

# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from .Notification import Notification


class NotificationNewGroupMembership(Notification):
    # Attributes
    id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    # Foreign keys
    group_membership_id = db.Column(db.Integer, db.ForeignKey('group_membership.id'))
    profile_id          = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    group_membership = db.relationship('GroupMembership')
    profile          = db.relationship('Profile')

    __mapper_args__ = {
        'polymorphic_identity': 'notificationNewGroupMembership',
    }

    def __init__(self, notification_owner_id, group_membership_id, profile_id):
        Notification.__init__(self, notification_owner_id)
        self.group_membership_id = group_membership_id
        self.profile_id          = profile_id

    def get_title(self):
        return u'¡Te han agregado a un grupo!'

    def get_description(self):
        description = u"%s te ha agregado al grupo \"%s\"." % (
            self.profile.first_name + " " + self.profile.last_name,
            self.group_membership.group.name,
        )
        return description

    @staticmethod
    def get_detail_object_type():
        return 'group'

    def get_detail_object_id(self):
        return self.group_membership.group.id

    def __repr__(self):
        return '<NotificationNewGroupMembership: %r>' % self.id

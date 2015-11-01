# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db


class GroupMembership(db.Model):
    # Attributes
    id       = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean)
    # Foreign keys
    group_id                 = db.Column(db.Integer, db.ForeignKey('group.id'))
    group_membership_type_id = db.Column(db.Integer, db.ForeignKey('group_membership_type.id'))
    permission_type_id       = db.Column(db.Integer, db.ForeignKey('permission_type.id'))
    profile_id               = db.Column(db.Integer, db.ForeignKey('profile.id'))
    # Relationships
    group                 = db.relationship('Group',
                                            backref=db.backref('memberships',
                                                               lazy='dynamic',
                                                               cascade='all, delete-orphan',
                                                               )
                                            )
    group_membership_type = db.relationship('GroupMembershipType',
                                            backref=db.backref('memberships', lazy='dynamic'))
    permission_type       = db.relationship('PermissionType',
                                            backref=db.backref('memberships', lazy='dynamic'))
    profile               = db.relationship('Profile',
                                            backref=db.backref('memberships', lazy='dynamic'))

    def __init__(self, is_admin, group_id, group_membership_type_id, permission_type_id, profile_id):
        self.is_admin                 = is_admin
        self.group_id                 = group_id
        self.group_membership_type_id = group_membership_type_id
        self.permission_type_id       = permission_type_id
        self.profile_id               = profile_id

    def __repr__(self):
        return '<GroupMembership: %r>' % self.id

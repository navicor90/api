# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger

from .groupFields import GroupFields
from .groupMembershipTypeFields import GroupMembershipTypeFields
from .permissionTypeFields import PermissionTypeFields
from .profileFields import ProfileFields


@swagger.model
@swagger.nested(group='GroupFields',
                group_membership_type='GroupMembershipTypeFields',
                permission_type='PermissionTypeFields',
                profile='ProfileFields')
class GroupMembershipFields:
    resource_fields = {
        'id': fields.Integer,
        'is_admin': fields.Boolean,
        'group': fields.Nested(GroupFields.resource_fields),
        'group_membership_type': fields.Nested(GroupMembershipTypeFields.resource_fields),
        'permission_type': fields.Nested(PermissionTypeFields.resource_fields),
        'profile': fields.Nested(ProfileFields.resource_fields),
    }

    required = [
        'id',
        'is_admin',
        'group',
        'group_membership_type',
        'permission_type',
        'profile',
    ]

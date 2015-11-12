# -*- coding: utf-8 -*-

from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class UserStatisticsFields:
    resource_fields = {
        'encryption_percentage': fields.Float,
    }

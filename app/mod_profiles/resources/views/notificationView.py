# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_shared.models.db import db
from app.mod_profiles.models import Notification
from app.mod_profiles.common.fields.notificationFields import NotificationFields
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_updated, code_401, code_403, \
    code_404


class NotificationView(Resource):
    @swagger.operation(
        notes=u'Marca como leída una instancia específica de notificación.'.encode('utf-8'),
        responseClass='NotificationFields',
        nickname='notificationView_put',
        parameters=[
            {
              "name": "notification_id",
              "description": u'Identificador único de la notificación.'.encode('utf-8'),
              "required": True,
              "dataType": "int",
              "paramType": "path"
            },
          ],
        responseMessages=[
            code_200_updated,
            code_401,
            code_403,
            code_404
        ]
    )
    @auth.login_required
    @marshal_with(NotificationFields.resource_fields, envelope='resource')
    def put(self, notification_id):
        # Obtiene la notificación.
        notification = Notification.query.get_or_404(notification_id)

        # Verifica que el usuario autenticado sea el dueño de la notificación
        # especificada.
        if g.user.id != notification.notification_owner.user.first().id:
            return '', 403

        # Marca la notificación como leída.
        notification.set_as_read()

        db.session.add(notification)
        db.session.commit()
        return notification, 200

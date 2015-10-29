# -*- coding: utf-8 -*-

from flask import g
from flask_restful import Resource, marshal_with
from flask_restful_swagger import swagger

from app.mod_shared.models.auth import auth
from app.mod_profiles.common.fields.notificationFields import NotificationFields
from app.mod_profiles.common.parsers.notification import parser_get
from app.mod_profiles.common.swagger.responses.generic_responses import code_200_found, code_401
from app.mod_profiles.models import Notification


class MyNotificationList(Resource):
    # Crea una copia de los campos de 'Notification'.
    resource_fields = NotificationFields.resource_fields.copy()
    # Quita el dueño de la notificación, de los campos del recurso.
    del resource_fields['notification_owner']

    @swagger.operation(
        # TODO: Añadir parámetros de autenticación a la documentación Swagger.
        notes=(u'Retorna todas las instancias existentes de notificación, '
               'asociadas al perfil del usuario autenticado, ordenadas por '
               'fecha y hora de creación.').encode('utf-8'),
        responseClass='NotificationFields',
        nickname='myNotificationList_get',
        parameters=[
            {
                "name": "quantity",
                "description": (u'Cantidad de notificaciones a retornar. '
                                'Por defecto, se retornan todas las '
                                'notificaciones.').encode('utf-8'),
                "required": False,
                "dataType": "int",
                "paramType": "query"
            },
            {
                "name": "unread",
                "description": (u'Variable booleana que indica si sólo se '
                                'deben retornar notificaciones no leídas. Por '
                                'defecto, se retornan leídas y no leídas.').encode('utf-8'),
                "required": False,
                "dataType": "boolean",
                "paramType": "query"
            },
        ],
        responseMessages=[
            code_200_found,
            code_401
        ]
    )
    @auth.login_required
    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        # Obtiene el perfil.
        profile = g.user.profile

        # Obtiene los valores de los argumentos recibidos en la petición.
        args = parser_get.parse_args()
        unread = args['unread']
        quantity = args['quantity']

        # Obtiene todas las notificaciones asociadas al perfil, y las ordena en
        # forma descendente por fecha y hora de creación.
        notifications = profile.notifications.order_by(Notification.created_datetime.desc())

        # Filtra las notificaciones, dejando sólo aquellas no leídas.
        if (unread is not None
                and unread):
            notifications = notifications.filter_by(read_datetime=None)
        # Limita la cantidad de notificaciones a retornar.
        if quantity is not None:
            notifications = notifications.limit(quantity)

        notifications = notifications.all()

        constructed_notifications = []

        # Arma las notificaciones, en base a los campos requeridos.
        for notification in notifications:
            constructed_notification = {
                'id': notification.id,
                'created_datetime': notification.created_datetime,
                'read_datetime': notification.read_datetime,
                'title': notification.get_title(),
                'description': notification.get_description(),
                'detail_object_type': notification.get_detail_object_type(),
                'detail_object_id': notification.get_detail_object_id(),
            }
            constructed_notifications.append(constructed_notification)

        return constructed_notifications

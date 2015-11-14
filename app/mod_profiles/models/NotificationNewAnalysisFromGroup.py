# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from .Notification import Notification


class NotificationNewAnalysisFromGroup(Notification):
    # Attributes
    id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    # Foreign keys
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))
    group_id    = db.Column(db.Integer, db.ForeignKey('group.id'))
    # Relationships
    analysis = db.relationship('Analysis',
                               backref=db.backref('notifications',
                                                  lazy='dynamic',
                                                  cascade='all, delete-orphan'
                                                  )
                               )
    group    = db.relationship('Group',
                               backref=db.backref('notifications',
                                                  lazy='dynamic',
                                                  cascade='all, delete-orphan',
                                                  )
                               )

    __mapper_args__ = {
        'polymorphic_identity': 'notificationNewAnalysisFromGroup',
    }

    def __init__(self, notification_owner_id, notification_author_id, analysis_id, group_id):
        Notification.__init__(self, notification_owner_id, notification_author_id)
        self.analysis_id = analysis_id
        self.group_id    = group_id

    def get_title(self):
        author = self.notification_author
        title = u'¡%s ha cargado un nuevo análisis en un grupo!' % (
            author.first_name + ' ' + author.last_name,
        )
        return title

    def get_description(self):
        description = (u'Un nuevo análisis, con el nombre "%s", ha sido '
                       'cargado en el grupo "%s".') % (
            self.analysis.description,
            self.group.name,
        )
        return description

    @staticmethod
    def get_detail_object_type():
        return 'analysis'

    def get_detail_object_id(self):
        return self.analysis.id

    @staticmethod
    def get_notification_type():
        return 'event'

    def __repr__(self):
        return '<NotificationNewAnalysisFromGroup: %r>' % self.id

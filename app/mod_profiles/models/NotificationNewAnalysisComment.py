# -*- coding: utf-8 -*-

from app.mod_shared.models.db import db
from .Notification import Notification


class NotificationNewAnalysisComment(Notification):
    # Attributes
    id = db.Column(db.Integer, db.ForeignKey('notification.id'), primary_key=True)
    # Foreign keys
    analysis_comment_id = db.Column(db.Integer, db.ForeignKey('analysis_comment.id'))
    # Relationships
    analysis_comment = db.relationship('AnalysisComment',
                                       backref=db.backref('notifications',
                                                          lazy='dynamic',
                                                          cascade='all, delete-orphan',
                                                          )
                                       )

    __mapper_args__ = {
        'polymorphic_identity': 'notificationNewAnalysisComment',
    }

    def __init__(self, notification_owner_id, notification_author_id, analysis_comment_id):
        Notification.__init__(self, notification_owner_id, notification_author_id)
        self.analysis_comment_id = analysis_comment_id

    def get_title(self):
        author = self.notification_author
        title = u'¡%s ha comentado un análisis tuyo!' % (
            author.first_name + ' ' + author.last_name,
        )
        return title

    def get_description(self):
        author = self.notification_author
        description = u'%s ha comentado en el análisis "%s".' % (
            author.first_name + " " + author.last_name,
            self.analysis_comment.analysis.description,
        )
        return description

    @staticmethod
    def get_detail_object_type():
        return 'analysis'

    def get_detail_object_id(self):
        return self.analysis_comment.analysis.id

    @staticmethod
    def get_notification_type():
        return 'message'

    def __repr__(self):
        return '<NotificationNewAnalysisComment: %r>' % self.id

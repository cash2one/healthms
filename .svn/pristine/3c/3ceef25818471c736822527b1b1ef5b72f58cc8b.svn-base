# encoding: utf8
from app import db
from datetime import datetime

class healthms_admins_info(db.Model):
    """docstring for healthms_admins_info"""
    admin_id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(50), nullable=False)
    admin_password = db.Column(db.String(50), nullable=False)
    admin_rank = db.Column(db.Integer, nullable=False)
    admin_login_date = db.Column(db.TIMESTAMP, default=datetime.utcnow(), nullable=False)
    admin_create_date = db.Column(db.TIMESTAMP, default=datetime.utcnow(), nullable=False)
    healthms_info = db.relationship('healthms_info', backref='admin', lazy='dynamic')

    def __init__(self, admin_username, admin_password, admin_rank):
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.admin_rank = admin_rank
        self.admin_login_date = admin_login_date
        self.admin_create_date = admin_create_date

class healthms_info(db.Model):
    """docstring for healthms_info"""
    info_id = db.Column(db.Integer, primary_key=True)
    info_type = db.Column(db.String(10), nullable=False)
    info_title = db.Column(db.String(50), nullable=False)
    info_content = db.Column(db.Text, nullable=False)
    info_hot = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('healthms_admins_info.admin_id'))
    info_edit_date = db.Column(db.TIMESTAMP, default=datetime.utcnow(), nullable=False)
    info_create_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, info_type, info_title, info_content, admin_id, info_hot=0, info_edit_date=datetime.utcnow(), info_create_date=datetime.utcnow()):
        self.info_type = info_type
        self.info_title = info_title
        self.info_content = info_content
        self.admin_id = admin_id
        self.info_hot = info_hot
        self.info_edit_date = info_edit_date
        self.info_create_date = info_create_date

        
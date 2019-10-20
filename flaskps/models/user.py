from datetime import datetime
from ..extensions.db import db
from . import user_role

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Integer, nullable=False, default=True)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    roles = db.relationship('Role', secondary=user_role, lazy='subquery',
        backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

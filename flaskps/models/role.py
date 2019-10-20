from ..extensions.db import db
from . import role_permission

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Permission', secondary=role_permission, lazy='subquery',
        backref=db.backref('role', lazy=True))

    def __repr__(self):
        return '<Role %r>' % self.name
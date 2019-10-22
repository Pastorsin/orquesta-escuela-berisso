from ..extensions.db import db
from . import role

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_role = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return ''
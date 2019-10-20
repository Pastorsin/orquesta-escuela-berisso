from ..extensions.db import db
from . import permission

class RolePermission(db.Model):
    __tablename__ = 'role_permission'
    id = db.Column(db.Integer, primary_key=True)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id'))
    id_permission = db.Column(db.Integer, db.ForeignKey('permission.id'))

    def __repr__(self):
        return ''
from flaskps.extensions.db import db
from flaskps.models.role import Role


user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey(
        'role.id'), primary_key=True)
)

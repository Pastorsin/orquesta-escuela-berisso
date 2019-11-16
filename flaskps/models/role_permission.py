from flaskps.extensions.db import db
from flaskps.models.permission import Permission


role_permission = db.Table(
    'role_permission',
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('role.id'),
        primary_key=True
    ),
    db.Column(
        'permission_id',
        db.Integer,
        db.ForeignKey('permission.id'),
        primary_key=True
    )
)

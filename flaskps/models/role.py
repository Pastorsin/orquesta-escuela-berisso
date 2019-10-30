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


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    permissions = db.relationship(
        'Permission',
        secondary=role_permission,
        lazy='subquery',
        backref=db.backref('roles', lazy=True)
    )

    def __repr__(self):
        return '<Role %r>' % self.name

    @classmethod
    def get_by_name(cls, rolname):
        return cls.query.filter_by(name=rolname).first()

    @classmethod
    def get_list_by_name(cls, rolnames):
        roles = map(lambda rolname: Role.get_by_name(rolname), rolnames)
        return list(roles)

    def has_permission(self, permission_name):
        permissions = map(
            lambda p: p.name == permission_name, self.permissions
        )
        return any(permissions)

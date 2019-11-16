import itertools
from flaskps.extensions.bcrypt import bcrypt as bc
from flaskps.extensions.db import db
from datetime import datetime
from flaskps.models.user_role import user_role


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    is_authenticated = db.Column(db.Boolean, nullable=False, default=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=False)

    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    roles = db.relationship('Role', secondary=user_role, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def __init__(self, data):
        self.__init_attributes(data)
        self.__init_hashes(data)
        self.__init_relationships(data)

    def __init_attributes(self, data):
        self.username = data['username']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']

    def __init_hashes(self, data):
        self.password = bc.generate_password_hash(data['password'])

    def __init_relationships(self, data):
        self.roles = data['roles']

    @classmethod
    def create(cls, data):
        user = cls(data)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def exist_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return bool(user)

    @classmethod
    def exist_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return bool(user)

    def __repr__(self):
        return '<User %r>' % self.username

    def validate_pass(self, candidate_pass):
        return bc.check_password_hash(self.password, candidate_pass)

    def get_id(self):
        return str(self.id)

    def activate(self):
        self.is_active = True
        db.session.commit()
        return self

    def deactivate(self):
        self.is_active = False
        db.session.commit()
        return self

    def update(self, values):
        self.__init_attributes(values)
        self.__init_relationships(values)
        db.session.commit()

    def has_permission(self, permission_name):
        permissions = map(lambda rol: rol.has_permission(permission_name), self.roles)
        return any(permissions)

    def permissions(self):
        roles_permissions = map(lambda rol: rol.permissions, self.roles)
        flat_permissions = itertools.chain(*roles_permissions)
        return set(flat_permissions)

from flaskps.extensions.bcrypt import bcrypt as bc
from flaskps.extensions.db import db
from datetime import datetime
from flaskps.models.role import Role


user_role = db.Table(
        'user_role',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    is_authenticated = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=False)

    updated_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    roles = db.relationship('Role', secondary=user_role, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username

    def validate_pass(self, candidate_pass):
        return bc.check_password_hash(self.password, candidate_pass)

    def get_id(self):
        return str(self.id)

    def activate(self):
        self.is_active=1
        db.session.commit()
        return self

    def deactivate(self):
        self.is_active=0
        db.session.commit()
        return self

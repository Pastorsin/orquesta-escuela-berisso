from ..extensions.db import db
from sqlalchemy import update


class Webconfig(db.Model):
    __tablename__ = 'webconfig'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    pagination = db.Column(
        db.Integer,
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False
    )

    frontend_enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    @classmethod
    def update(cls, config):
        update_sql = update(cls, values=config)
        db.session.execute(update_sql)
        db.session.commit()

    def __repr__(self):
        return self.__tablename__

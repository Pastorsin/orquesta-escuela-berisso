from ..extensions.db import db


class Webconfig(db.Model):
    __tablename__ = 'webconfig'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    value = db.Column(db.Text)

    def __repr__(self):
        return ''

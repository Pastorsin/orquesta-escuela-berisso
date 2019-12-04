from flaskps.extensions.db import db


class Instrument(db.Model):

    __tablename__ = 'instrumento'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        'nombre',
        db.String(255),
        nullable=False
    )

    category = db.Column(
        'categoria',
        db.String(255),
        nullable=False
    )

    inventory_number = db.Column(
        'cod_inventario',
        db.String(255),
        unique=True,
        nullable=False
    )

    image = db.Column(
        'imagen',
        db.LargeBinary(length=(2**32) - 1),
        nullable=False
    )

    def __repr__(self):
        return f"{self.inventory_number} - {self.name}"

    def __init__(self, data):
        self.__init_attributes(data)

    def __init_attributes(self, data):
        self.name = data['name']
        self.category = data['category']
        self.inventory_number = data['inventory_number']
        self.image = data['image']

    @classmethod
    def create(cls, data):
        instrument = cls(data)
        db.session.add(instrument)
        db.session.commit()

    @classmethod
    def any_inventory_number(cls, number):
        return any(
            cls.query.filter(cls.inventory_number == number)
        )

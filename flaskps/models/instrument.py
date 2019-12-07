from flaskps.extensions.db import db
from flaskps.models.instrument_type import InstrumentType


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

    category_id = db.Column(
        'categoria_id',
        db.Integer,
        db.ForeignKey('tipo_instrumento.id'),
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

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):
        return f"{self.inventory_number} - {self.name}"

    def __init__(self, data):
        self.__init_attributes(data)
        self.__init_image(data)

    def __init_attributes(self, data):
        self.name = data['name']
        self.category_id = data['category_id']
        self.inventory_number = data['inventory_number']

    def __init_image(self, data):
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
        db.session.commit()

    def update_image(self, values):
        self.__init_image(values)
        db.session.commit()

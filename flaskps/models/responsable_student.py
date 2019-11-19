from flaskps.extensions.db import db


responsable_student = db.Table(
    'responsable_estudiante',
    db.Column(
        'estudiante_id',
        db.Integer,
        db.ForeignKey('estudiante.id'),
        primary_key=True
    ),
    db.Column(
        'responsable_id',
        db.Integer,
        db.ForeignKey('responsable.id'),
        primary_key=True
    )
)

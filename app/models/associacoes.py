from app import db

ninhada_filhote = db.Table('ninhada_filhote',
    db.Column('ninhada_id', db.Integer, db.ForeignKey('ninhadas.id'), primary_key=True),
    db.Column('ave_id', db.Integer, db.ForeignKey('aves.id'), primary_key=True)
) 
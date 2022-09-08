# when adding new columns to a database, we need to migrate. this is not a trivial
# procedure for me, so I needed here flask_migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from mynewapp import app, db, User, Sesion, 



class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    AIinspiration = db.Column(db.String(300), nullable=True)
    prompt = db.Column(db.Text, nullable=True)
    tokens_usados = db.Column(db.Integer, nullable=False, default=0)
    prompt_tokens = db.Column(db.Integer, nullable=False, default=0)
    historia = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    #story=db.Column(JSON, nullable=True)
    sesion_id = db.Column(db.Integer, db.ForeignKey('sesion.id'),
        nullable=False)
    sesion = db.relationship('Sesion',
        backref=db.backref('historias', lazy=True))

    def __repr__(self):
        return '<Historia: %r>' % self.titulo

# [SQL: ALTER TABLE historia ADD COLUMN prompt_tokens INTEGER NOT NULL]



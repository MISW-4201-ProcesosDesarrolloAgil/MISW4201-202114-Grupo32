from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime

import enum


db = SQLAlchemy()

albumes_canciones = db.Table('album_cancion',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

albumes_compartidos = db.Table('albumes_compartidos',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True))

canciones_compartidas = db.Table('canciones_compartidas',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

# # Usuarios que comentan 
# usuarios_comentarios = db.Table('usuarios_comentarios',
#     db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True),
#     db.Column('comentario_id', db.Integer, db.ForeignKey('comentario.id'), primary_key = True))
# # Albumes con comentarios
# albumes_comentarios = db.Table('albumes_comentarios',
#     db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
#     db.Column('comentario_id', db.Integer, db.ForeignKey('comentario.id'), primary_key = True))

class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    albumes = db.relationship('Album', secondary = 'album_cancion', back_populates="canciones")
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    compartido_a = db.relationship('Usuario', secondary = 'canciones_compartidas', back_populates="canciones_compartidas")

class Medio(enum.Enum):
   DISCO = 1
   CASETE = 2
   CD = 3

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates="albumes")
    compartido_a = db.relationship('Usuario', secondary = 'albumes_compartidos', back_populates="albumes_compartidos")
    # comentarios = db.relationship('Comentario', secondary = 'albumes_comentarios', back_populates="album")
    comentarios = db.relationship('ComentarioAlbum', cascade='all, delete, delete-orphan')


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')
    albumes_compartidos = db.relationship('Album', secondary = 'albumes_compartidos', back_populates="compartido_a")
    canciones_compartidas = db.relationship('Cancion', secondary = 'canciones_compartidas', back_populates="compartido_a")
    # comentarios = db.relationship('Comentario', secondary = 'usuarios_comentarios', back_populates="usuario")


class ComentarioAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(255))
    fecha = db.Column(db.String(50))
    usuario = db.Column(db.Integer)
    album = db.Column(db.Integer, db.ForeignKey('album.id'))
    # album = db.relationship("Album", back_populates="comentarios")
    
    # usuario = db.relationship("Usuario", back_populates="comentarios")

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Cancion
         include_relationships = True
         load_instance = True

class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=("medio"))
    class Meta:
         model = Album
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class ComentarioAlbumSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = ComentarioAlbum
         include_relationships = True
         load_instance = True
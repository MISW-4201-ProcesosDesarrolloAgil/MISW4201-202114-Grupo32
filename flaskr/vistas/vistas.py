from re import A
from flask import request
from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, ComentarioAlbum, ComentarioAlbumSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import logging

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
comentario_album_schema = ComentarioAlbumSchema()
album_schema = AlbumSchema()

class VistaCanciones(Resource):
    @jwt_required()
    def post(self, id_usuario):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"],
                                segundos=request.json["segundos"], interprete=request.json["interprete"])
        Usuario.query.get_or_404(id_usuario)
        nueva_cancion.usuario = id_usuario
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self, id_usuario):
        return [cancion_schema.dump(ca) for ca in Cancion.query.all() if id_usuario == ca.usuario]


class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    @jwt_required()
    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo", cancion.titulo)
        cancion.minutos = request.json.get("minutos", cancion.minutos)
        cancion.segundos = request.json.get("segundos", cancion.segundos)
        cancion.interprete = request.json.get("interprete", cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    @jwt_required()
    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '', 204


class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]


class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(
            nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso}

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(
            Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


class VistaAlbumsUsuario_implementacion:

    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"],
                            descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre', 409

        return album_schema.dump(nuevo_album)

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]


class VistaCompartirAlbum_Implementacion:
    def post(self, id_album, id_usuarios):
        album = Album.query.get_or_404(id_album)
        usuarios = [Usuario.query.get_or_404(
            id_usuario) for id_usuario in id_usuarios]
        for usuario in usuarios:
            if any(compartido.id == usuario.id for compartido in album.compartido_a):
                db.session.rollback()
                return f"Error: El album {album.titulo} ya fue compartido a {usuario.nombre}.", 409

            if album.usuario == usuario.id:
                db.session.rollback()
                return f"Error: No se puedes compartir un album a su mismo propietario.", 409

            album.compartido_a.append(usuario)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'Se generó un error al tratar de compartir el album', 409

        return album_schema.dump(album)

#:-: Crear Album
class VistaAlbumsUsuario(VistaAlbumsUsuario_implementacion, Resource):
    @jwt_required()
    def post(self, id_usuario):
        return super().post(id_usuario)

    def get(self, id_usuario):
        return super().get(id_usuario)

# :-:
class VistaAlbumsCompartidosUsuario_implementacion(Resource):
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        albums = []
        for al in usuario.albumes_compartidos:
            album_compartido = album_schema.dump(al) 
            album_compartido["nombre_dueno"] = Usuario.query.get(al.usuario).nombre
            albums.append(album_compartido)
        return albums

class VistaCancionesCompartidosUsuario_implementacion(Resource):
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        canciones = []
        for al in usuario.canciones_compartidas:
            cancion_compartida = cancion_schema.dump(al) 
            cancion_compartida["nombre_dueno"] = Usuario.query.get(al.usuario).nombre
            canciones.append(cancion_compartida)
        return canciones


class VistaAlbumsCompartidosUsuario(VistaAlbumsCompartidosUsuario_implementacion, Resource):
    @jwt_required()
    def get(self, id_usuario):
        return super().get(id_usuario)


class VistaCancionesCompartidosUsuario(VistaCancionesCompartidosUsuario_implementacion, Resource):
    @jwt_required()
    def get(self, id_usuario):
        return super().get(id_usuario)


class VistaCompartirAlbum(VistaCompartirAlbum_Implementacion, Resource):
    @jwt_required()
    def post(self, id_album):
        return super().post(id_album, request.json["id_usuarios"])


class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)

        if "id_cancion" in request.json.keys():

            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea', 404
        else:
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"],
                                    segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]


class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo", album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '', 204


def info_usuario_simple(usuario):
    return {"id": usuario.id, "nombre": usuario.nombre}


class VistaUsuarios_Implementacion:
    def get(self):
        return [info_usuario_simple(us) for us in Usuario.query.all()]


class VistaUsuarios(VistaUsuarios_Implementacion, Resource):
    @jwt_required()
    def get(self):
        return super().get()

class VistaCompartirCancion_Implementacion:
    def post(self, id_cancion, id_usuarios):
        cancion = Cancion.query.get_or_404(id_cancion)
        usuarios = [Usuario.query.get_or_404(id_usuario) for id_usuario in id_usuarios]
        for usuario in usuarios:
            if any(compartido.id == usuario.id for compartido in cancion.compartido_a):
                db.session.rollback()
                return f"Error: El album {cancion.titulo} ya fue compartido a {usuario.nombre}.", 409

            if cancion.usuario == usuario.id:
                db.session.rollback()
                return f"Error: No se puedes compartir una cacion a su mismo propietario.", 409

            cancion.compartido_a.append(usuario)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'Se generó un error al tratar de compartir la cacion', 409

        return cancion_schema.dump(cancion)

class VistaCompartirCancion(VistaCompartirCancion_Implementacion, Resource):
    @jwt_required()
    def post(self, id_cancion):
        return super().post(id_cancion, request.json["id_usuarios"])


# 


class VistaComentarioAlbum_implementacion:
    
    def post(self, id_album):
        usuario = Usuario.query.get_or_404(request.json["usuario_id"])
        alb = Usuario.query.get_or_404(request.json["album_id"])
        # album = Usuario.query.get_or_404(request.json["album_id"])


        
        nuevo_comentario = ComentarioAlbum(comentario=request.json["comentario"], fecha=request.json["fecha"],
                            usuario=usuario.id, album=alb.id  )
        album = Album.query.get_or_404(id_album)
        album.comentarios.append(nuevo_comentario)

        db.session.commit()
        return comentario_album_schema.dump(nuevo_comentario)

    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        lista_comentario = []

        for comentario in album.comentarios:
            comentario_album = comentario_album_schema.dump(comentario) 
            comentario_album["nombre_usuario"] = Usuario.query.get(comentario.usuario).nombre
            lista_comentario.append(comentario_album)

        return lista_comentario


class VistaComentarAlbum(VistaComentarioAlbum_implementacion, Resource):
    @jwt_required()
    def post(self, id_album):
        return super().post(id_album)

    def get(self, id_album):
        return super().get(id_album)


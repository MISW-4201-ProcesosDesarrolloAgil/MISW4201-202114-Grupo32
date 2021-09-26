from flaskr.vistas.vistas import VistaCancionesCompartidosUsuario_implementacion
import unittest
from flaskr.modelos.modelos import Medio
from flaskr.modelos import Album, db, Cancion, Usuario
from flaskr.vistas import VistaAlbumsCompartidosUsuario
from faker import Faker

import flaskr.app


__author__ = "Luis León"
__copyright__ = "Luis León"
__license__ = "mit"

def limpiar_db():
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        db.session.delete(usuario)

    canciones = Cancion.query.all()
    for cancion in canciones:
        db.session.delete(cancion)
    db.session.commit()

class test_vista_compartir_album(unittest.TestCase):

    def __init__(self, methodName):
        self.generador_datos = Faker()
        Faker.seed(2000)
        self.vista_canciones_compartidas = VistaCancionesCompartidosUsuario_implementacion()
        super().__init__(methodName=methodName)

    def test_obtener_lista(self):
        canciones_usuarios = self.vista_canciones_compartidas.get(self.usuario2.id)
        self.assertTrue(isinstance(canciones_usuarios, list))

    def test_lista_vacia(self):
        canciones_usuarios = self.vista_canciones_compartidas.get(self.usuario1.id)
        self.assertTrue(isinstance(canciones_usuarios, list))

    def setUp(self):
        limpiar_db()

        self.usuario1 = Usuario(nombre=self.generador_datos.unique.first_name(
        ), contrasena=self.generador_datos.password())
        self.usuario2 = Usuario(nombre = self.generador_datos.unique.first_name(
        ), contrasena=self.generador_datos.password())
        self.usuario3 = Usuario(nombre = self.generador_datos.unique.first_name(
        ), contrasena=self.generador_datos.password())

        db.session.add(self.usuario1)
        db.session.add(self.usuario2)
        db.session.add(self.usuario3)

        db.session.commit()

        self.cancion = Cancion(
            titulo = self.generador_datos.unique.first_name(),
            minutos = 4,
            segundos = 15,
            interprete = self.generador_datos.unique.first_name(),
            usuario = self.usuario1.id
        )

        self.cancion2 = Cancion(
            titulo = self.generador_datos.unique.first_name(),
            minutos = 3,
            segundos = 30,
            interprete = self.generador_datos.unique.first_name(),
            usuario = self.usuario1.id
        )

        db.session.add(self.cancion)
        db.session.add(self.cancion2)

        db.session.commit()

    def tearDown(self):
        limpiar_db()
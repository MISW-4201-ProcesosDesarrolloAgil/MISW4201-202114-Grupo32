from flaskr.modelos.modelos import Medio
from flaskr.modelos import Album, db, Cancion, Usuario
import unittest
from flaskr.vistas import VistaCompartirCancion_Implementacion
from faker import Faker

# iniciar el app
import flaskr.app

__author__ = "Anderson Luis Cáceres Padilla"
__copyright__ = "Anderson Luis Cáceres Padilla"
__license__ = "mit"


def limpiar_db():
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        db.session.delete(usuario)

    canciones = Cancion.query.all()
    for cancion in canciones:
        db.session.delete(cancion)
    db.session.commit()

class test_vista_compartir_cancion(unittest.TestCase):
    def __init__(self, methodName):
        self.generador_datos = Faker()
        Faker.seed(2000)
        self.vista = VistaCompartirCancion_Implementacion()
        super().__init__(methodName=methodName)


    def test_compartir_cancion_satisfactoriamente(self):
        id_usuarios = [self.usuario2.id, self.usuario3.id]

        result = self.vista.post(self.cancion.id, id_usuarios)

        compartido = [usuario for usuario in self.cancion.compartido_a if usuario.id in id_usuarios]

        self.assertEqual(len(compartido), 2)
        self.assertEqual(len(self.usuario2.canciones_compartidas), 1)
        self.assertTrue(self.cancion in self.usuario2.canciones_compartidas)
        self.assertEqual(len(self.usuario3.canciones_compartidas),1)
        self.assertTrue(self.cancion in self.usuario3.canciones_compartidas)

        self.assertEqual(len(self.cancion2.compartido_a), 0)
        result = self.vista.post(self.cancion2.id, [self.usuario3.id])

        self.assertTrue(len(self.cancion2.compartido_a), 1)
        self.assertTrue(self.usuario3 in self.cancion2.compartido_a)
        
        self.assertEqual(len(self.usuario3.canciones_compartidas), 2)
        self.assertTrue(self.cancion2 in self.usuario3.canciones_compartidas)

    def test_intenter_compartir_cancion_a_dueno(self):
        result = self.vista.post(self.cancion.id,[self.usuario1.id])
        self.assertEqual(result[1], 409)
        self.assertEqual(len(self.usuario1.canciones_compartidas), 0)
        self.assertEqual(len(self.cancion.compartido_a), 0)

    def test_dos_veces_al_mismo_usuario(self):
        result = self.vista.post(self.cancion.id,[self.usuario2.id])

        result = self.vista.post(self.cancion.id,[self.usuario2.id])
        self.assertEqual(result[1], 409)
        self.assertEqual(len(self.usuario2.canciones_compartidas), 1)
        self.assertEqual(len(self.cancion.compartido_a), 1)

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

from flaskr.modelos.modelos import Medio
from flaskr.modelos import Album, db, Cancion, Usuario
import unittest
from flaskr.vistas import VistaCompartirAlbum_Implementacion
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


class test_vista_compartir_album(unittest.TestCase):

    def __init__(self, methodName):
        self.generador_datos = Faker()
        Faker.seed(2000)
        self.vista = VistaCompartirAlbum_Implementacion()
        super().__init__(methodName=methodName)

    def test_compartir_album_satisfactoriamente(self):
        id_usuarios = [self.usuario2.id, self.usuario3.id]

        result = self.vista.post(self.album.id, id_usuarios)

        compartido = [usuario for usuario in self.album.compartido_a if usuario.id in id_usuarios]

        self.assertEqual(len(compartido), 2)
        self.assertTrue(len(self.usuario2.albumes_compartidos) == 1 and self.album in self.usuario2.albumes_compartidos)
        self.assertEqual(len(self.usuario3.albumes_compartidos), 1)
        self.assertTrue(self.album in self.usuario3.albumes_compartidos)

        self.assertEqual(len(self.album2.compartido_a), 0)
        result = self.vista.post(self.album2.id, [self.usuario3.id])

        self.assertEqual(len(self.album2.compartido_a), 1)
        self.assertTrue(self.usuario3 in self.album2.compartido_a)
        
        self.assertEqual(len(self.usuario3.albumes_compartidos), 2)
        self.assertTrue(self.album2 in self.usuario3.albumes_compartidos)

    def test_intenter_compartir_album_a_dueno(self):
        result = self.vista.post(self.album.id,[self.usuario1.id])
        self.assertEqual(result[1], 409)
        self.assertEqual(len(self.usuario1.albumes_compartidos), 0)
        self.assertEqual(len(self.album.compartido_a), 0)

    def test_dos_veces_al_mismo_usuario(self):
        result = self.vista.post(self.album.id,[self.usuario2.id])

        result = self.vista.post(self.album.id,[self.usuario2.id])
        self.assertEqual(result[1], 409)
        self.assertEqual(len(self.usuario2.albumes_compartidos), 1)
        self.assertEqual(len(self.album.compartido_a), 1)

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

        self.album = Album(
            titulo=self.generador_datos.unique.first_name(),
            anio=2020,
            descripcion=self.generador_datos.text(),
            medio=Medio.CD,
        )

        self.album2 = Album(
            titulo=self.generador_datos.unique.first_name(),
            anio=2020,
            descripcion=self.generador_datos.text(),
            medio=Medio.CD,
        )

        self.usuario1.albumes.append(self.album)
        self.usuario1.albumes.append(self.album2)

        db.session.commit()

    def tearDown(self):
        limpiar_db()
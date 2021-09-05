import unittest
from flaskr.vistas import VistaUsuarios
from flaskr.modelos import db, Cancion, Usuario
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


class test_vista_usuario(unittest.TestCase):

    def __init__(self, methodName):
        self.numero_usuarios_test = 5
        self.generador_datos = Faker()
        Faker.seed(2000)
        self.vista_usuarios = VistaUsuarios()
        super().__init__(methodName=methodName)

    # Validar lista
    def test_obtener_lista(self):
        usuarios = self.vista_usuarios.get()
        self.assertTrue(isinstance(usuarios, list))
    
    # Validar cada usuario optenido
    def test_usuarios_validos(self):
        usuarios = self.vista_usuarios.get()
        usuarios_validados = set([])
        for usuario_a_validar in usuarios:
            id = usuario_a_validar["id"]
            self.assertFalse(id in usuarios_validados)
            usuarios_validados.add(id)
            usuario_real = self.usuarios_dic[id]
            self.assertEqual(usuario_real.nombre,
                             usuario_a_validar.get("nombre"))
            self.assertEqual(
                usuario_real.contrasena, usuario_a_validar.get("contrasena"))

            self.assertTrue(isinstance(usuario_a_validar.get("albumes"), list))

        self.assertEqual(len(usuarios_validados), self.numero_usuarios_test)

    def setUp(self):
        limpiar_db()

        usuarios = []
        for i in range(self.numero_usuarios_test):
            usuario_prueba = Usuario(nombre=self.generador_datos.unique.first_name(
            ), contrasena=self.generador_datos.password())
            usuarios.append(usuario_prueba)
            db.session.add(usuario_prueba)

        db.session.commit()
        self.usuarios_dic = {
            usuario.id: usuario for usuario in usuarios}

    def tearDown(self):
        limpiar_db()

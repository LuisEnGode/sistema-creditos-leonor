# Create your tests here.
from django.db import IntegrityError
from django.test import TestCase

from apps.clientes.models import Cliente


class ClienteModelTests(TestCase):
    def test_crear_cliente(self):
        cliente = Cliente.objects.create(
            tipo_identificacion="cedula",
            identificacion="0102030405",
            nombres="Jonathan",
            apellidos="Loja",
            telefono="0999999999",
            correo="jonathan@example.com",
            direccion="Cuenca",
        )

        self.assertEqual(cliente.identificacion, "0102030405")
        self.assertEqual(cliente.nombres, "Jonathan")
        self.assertEqual(cliente.apellidos, "Loja")
        self.assertTrue(cliente.activo)

    def test_identificacion_debe_ser_unica(self):
        Cliente.objects.create(
            identificacion="0102030405",
            nombres="Jonathan",
            apellidos="Loja",
        )

        with self.assertRaises(IntegrityError):
            Cliente.objects.create(
                identificacion="0102030405",
                nombres="Otro",
                apellidos="Cliente",
            )

    def test_str_cliente(self):
        cliente = Cliente.objects.create(
            identificacion="0102030405",
            nombres="Jonathan",
            apellidos="Loja",
        )

        self.assertEqual(
            str(cliente),
            "Loja Jonathan - 0102030405",
        )


class ClienteApiTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            tipo_identificacion="cedula",
            identificacion="0102030405",
            nombres="Jonathan",
            apellidos="Loja",
            telefono="0999999999",
            correo="jonathan@example.com",
        )

    def test_listar_clientes(self):
        response = self.client.get("/api/clientes/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["identificacion"],
            "0102030405",
        )

    def test_obtener_cliente(self):
        response = self.client.get(
            f"/api/clientes/{self.cliente.id}",
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["nombres"], "Jonathan")
        self.assertEqual(data["apellidos"], "Loja")

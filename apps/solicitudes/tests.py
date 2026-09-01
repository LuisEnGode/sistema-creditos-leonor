from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from apps.clientes.models import Cliente
from apps.solicitudes.models import SolicitudCredito


class SolicitudCreditoModelTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            identificacion="0102030405",
            nombres="Jonathan",
            apellidos="Loja",
        )

    def test_credito_comercial_permite_cliente_no_socio(self):
        solicitud = SolicitudCredito(
            cliente=self.cliente,
            tipo_credito=SolicitudCredito.TipoCredito.COMERCIAL,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
        )

        solicitud.full_clean()

        self.assertEqual(
            solicitud.tipo_credito,
            SolicitudCredito.TipoCredito.COMERCIAL,
        )

    def test_credito_consumo_requiere_cliente_socio(self):
        solicitud = SolicitudCredito(
            cliente=self.cliente,
            tipo_credito=SolicitudCredito.TipoCredito.CONSUMO,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
        )
        mensaje = (
            "Los créditos de consumo solamente pueden solicitarse para clientes socios."
        )

        with self.assertRaisesMessage(ValidationError, mensaje):
            solicitud.full_clean()

    def test_credito_consumo_permite_cliente_socio(self):
        self.cliente.es_socio = True
        self.cliente.save(update_fields=["es_socio"])

        solicitud = SolicitudCredito(
            cliente=self.cliente,
            tipo_credito=SolicitudCredito.TipoCredito.CONSUMO,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
        )

        solicitud.full_clean()

        self.assertEqual(
            solicitud.tipo_credito,
            SolicitudCredito.TipoCredito.CONSUMO,
        )

    def test_crear_solicitud(self):
        solicitud = SolicitudCredito.objects.create(
            cliente=self.cliente,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
            observaciones="Solicitud inicial",
        )

        self.assertEqual(
            solicitud.monto_solicitado,
            Decimal("2000.00"),
        )
        self.assertEqual(solicitud.plazo_meses, 24)
        self.assertEqual(
            solicitud.estado,
            SolicitudCredito.Estado.BORRADOR,
        )
        self.assertEqual(
            solicitud.tipo_credito,
            SolicitudCredito.TipoCredito.POR_DEFINIR,
        )
        self.assertIsNotNone(solicitud.fecha_solicitud)

    def test_monto_debe_ser_mayor_que_cero(self):
        solicitud = SolicitudCredito(
            cliente=self.cliente,
            monto_solicitado=Decimal("0.00"),
            plazo_meses=24,
        )

        with self.assertRaises(ValidationError):
            solicitud.full_clean()

    def test_plazo_debe_ser_mayor_que_cero(self):
        solicitud = SolicitudCredito(
            cliente=self.cliente,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=0,
        )

        with self.assertRaises(ValidationError):
            solicitud.full_clean()

    def test_cliente_con_solicitud_no_se_puede_eliminar(self):
        SolicitudCredito.objects.create(
            cliente=self.cliente,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
        )

        with self.assertRaises(ProtectedError):
            self.cliente.delete()

    def test_str_solicitud(self):
        solicitud = SolicitudCredito.objects.create(
            cliente=self.cliente,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
        )

        self.assertEqual(
            str(solicitud),
            (f"Solicitud #{solicitud.id} - Loja Jonathan - 0102030405 - $2000.00"),
        )


class SolicitudCreditoApiTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            identificacion="0102030405",
            nombres="Jonathan",
            apellidos="Loja",
        )
        self.solicitud = SolicitudCredito.objects.create(
            cliente=self.cliente,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
            observaciones="Solicitud inicial",
        )

    def test_listar_solicitudes(self):
        response = self.client.get("/api/solicitudes/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.solicitud.id)
        self.assertEqual(data[0]["cliente_id"], self.cliente.id)
        self.assertEqual(data[0]["monto_solicitado"], "2000.00")
        self.assertEqual(
            data[0]["tipo_credito"],
            SolicitudCredito.TipoCredito.POR_DEFINIR,
        )

    def test_obtener_solicitud(self):
        response = self.client.get(
            f"/api/solicitudes/{self.solicitud.id}",
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["id"], self.solicitud.id)
        self.assertEqual(data["estado"], SolicitudCredito.Estado.BORRADOR)
        self.assertEqual(data["plazo_meses"], 24)

    def test_obtener_solicitud_inexistente(self):
        response = self.client.get("/api/solicitudes/999999")

        self.assertEqual(response.status_code, 404)

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.clientes.models import Cliente
from apps.creditos.models import Credito
from apps.solicitudes.models import SolicitudCredito


class CreditoModelTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Ana",
            apellidos="Mora",
            identificacion="0102030405",
            es_socio=True,
        )

    def crear_solicitud(
        self,
        *,
        estado=SolicitudCredito.Estado.APROBADA,
        tipo_credito=SolicitudCredito.TipoCredito.COMERCIAL,
    ):
        return SolicitudCredito.objects.create(
            cliente=self.cliente,
            tipo_credito=tipo_credito,
            monto_solicitado=Decimal("2000.00"),
            plazo_meses=24,
            estado=estado,
        )

    def test_credito_calcula_gasto_administrativo_y_ahorro(self):
        solicitud = self.crear_solicitud()

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=24,
            tasa_interes_anual=Decimal("15.00"),
        )

        self.assertEqual(
            credito.gasto_administrativo,
            Decimal("40.0000"),
        )
        self.assertEqual(
            credito.ahorro,
            Decimal("100.0000"),
        )
        self.assertEqual(
            credito.descuentos_iniciales,
            Decimal("140.0000"),
        )

    def test_credito_calcula_monto_desembolsado(self):
        solicitud = self.crear_solicitud()

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=24,
            tasa_interes_anual=Decimal("15.00"),
        )

        self.assertEqual(
            credito.monto_desembolsado,
            Decimal("1860.0000"),
        )

    def test_solicitud_aprobada_puede_generar_credito(self):
        solicitud = self.crear_solicitud()

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=24,
            tasa_interes_anual=Decimal("15.00"),
        )

        credito.full_clean()

    def test_solicitud_no_aprobada_no_puede_generar_credito(self):
        solicitud = self.crear_solicitud(
            estado=SolicitudCredito.Estado.PENDIENTE,
        )

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=24,
            tasa_interes_anual=Decimal("15.00"),
        )

        with self.assertRaises(ValidationError):
            credito.full_clean()

    def test_tipo_por_definir_no_puede_generar_credito(self):
        solicitud = self.crear_solicitud(
            tipo_credito=SolicitudCredito.TipoCredito.POR_DEFINIR,
        )

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=24,
            tasa_interes_anual=Decimal("15.00"),
        )

        with self.assertRaises(ValidationError):
            credito.full_clean()

    def test_credito_no_permite_plazo_menor_a_un_mes(self):
        solicitud = self.crear_solicitud()

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=0,
            tasa_interes_anual=Decimal("15.00"),
        )

        with self.assertRaises(ValidationError):
            credito.full_clean()

    def test_credito_no_permite_tasa_interes_negativa(self):
        solicitud = self.crear_solicitud()

        credito = Credito(
            solicitud=solicitud,
            monto_original=Decimal("2000.00"),
            plazo_meses=24,
            tasa_interes_anual=Decimal("-1.00"),
        )

        with self.assertRaises(ValidationError):
            credito.full_clean()

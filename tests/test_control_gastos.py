import unittest
from datetime import date
from decimal import Decimal

from control_gastos import Gasto, agregar_gasto, calcular_total, convertir_monto
from app import app as flask_app


class TestControlGastos(unittest.TestCase):
    def test_convierte_monto_valido(self):
        self.assertEqual(convertir_monto("125.50"), Decimal("125.50"))

    def test_rechaza_monto_invalido_o_no_positivo(self):
        for valor in ("abc", "0", "-2", "NaN", "Infinity"):
            with self.subTest(valor=valor):
                with self.assertRaises(ValueError):
                    convertir_monto(valor)

    def test_agrega_gasto_y_limpia_descripcion(self):
        gastos = []
        gasto = agregar_gasto(gastos, "  Transporte  ", Decimal("30.00"), "Transporte")
        self.assertEqual(gasto, Gasto("Transporte", Decimal("30.00"), date.today(), "Transporte"))
        self.assertEqual(gastos, [gasto])

    def test_rechaza_descripcion_vacia(self):
        with self.assertRaises(ValueError):
            agregar_gasto([], "   ", Decimal("10"), "Otros")

    def test_calcula_total_de_gastos(self):
        gastos = [
            Gasto("Comida", Decimal("120.25"), date.today(), "Comida"),
            Gasto("Transporte", Decimal("35.75"), date.today(), "Transporte"),
        ]
        self.assertEqual(calcular_total(gastos), Decimal("156.00"))

    def test_total_de_lista_vacia_es_cero(self):
        self.assertEqual(calcular_total([]), Decimal("0"))


class TestAplicacionWeb(unittest.TestCase):
    def setUp(self):
        flask_app_module = __import__("app")
        flask_app_module.gastos_registrados.clear()
        flask_app.config["TESTING"] = True
        self.client = flask_app.test_client()

    def tearDown(self):
        flask_app_module = __import__("app")
        flask_app_module.gastos_registrados.clear()

    def test_pagina_principal_carga_correctamente(self):
        respuesta = self.client.get("/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"v1.2.0", respuesta.data)
        self.assertIn(b"Gastos registrados", respuesta.data)

    def test_post_valido_agrega_gasto_y_actualiza_total(self):
        respuesta = self.client.post(
            "/",
            data={"descripcion": "Almuerzo", "monto": "25.50", "categoria": "Comida"},
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"Almuerzo", respuesta.data)
        self.assertIn(b"$25.50", respuesta.data)
        self.assertIn(b">1<", respuesta.data)

    def test_post_invalido_muestra_error_sin_guardar(self):
        for monto in ("texto", "0", "-1"):
            with self.subTest(monto=monto):
                respuesta = self.client.post(
                    "/",
                    data={"descripcion": "Gasto", "monto": monto},
                )

                self.assertEqual(respuesta.status_code, 400)
                self.assertIn(b"El monto", respuesta.data)

    def test_limpiar_vacia_la_lista_de_gastos(self):
        self.client.post(
            "/",
            data={"descripcion": "Taxi", "monto": "12", "categoria": "Transporte"},
        )

        respuesta = self.client.post("/limpiar")

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"No hay gastos registrados.", respuesta.data)
        self.assertIn(b">0<", respuesta.data)

    def test_health_devuelve_estado_y_contador(self):
        respuesta = self.client.get("/health")

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.get_json(),
            {"status": "ok", "version": "1.2.0", "gastos_count": 0},
        )

    def test_respuesta_incluye_cabeceras_seguras(self):
        respuesta = self.client.get("/")

        self.assertEqual(respuesta.headers["Cache-Control"], "no-store")
        self.assertEqual(respuesta.headers["X-Content-Type-Options"], "nosniff")


if __name__ == "__main__":
    unittest.main()

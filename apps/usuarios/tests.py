from django.test import TestCase


class SimpleTest(TestCase):
    """Clase de prueba simple para verificar la configuración."""

    def test_basic_assertion(self):
        """
        Prueba que una aserción básica (True es True) funciona.
        Este es un test 'humo' para asegurar que el runner funciona.
        """
        self.assertTrue(True)

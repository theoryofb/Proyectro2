import unittest
from unittest.mock import patch, MagicMock
from datetime import date, time
import tui


# ---------- OBJETO FALSO TIPO PEEWEE ----------
class FakeEvento:
    def __init__(self, id, tipo, nombre, carnet, direccion_domicilio,
                 monto_garantia, monto_total, dia, hora_fin, decoracion):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre
        self.carnet = carnet
        self.direccion_domicilio = direccion_domicilio
        self.monto_garantia = monto_garantia
        self.monto_total = monto_total
        self.dia = dia
        self.hora_fin = hora_fin
        self.decoracion = decoracion
        self.conflicto = False


# ---------- INICIO DE TESTS ----------
class TestTUI(unittest.TestCase):

    # Evita que pause() y clear_screen() afecten
    @patch("tui.pause", lambda: None)
    @patch("tui.clear_screen", lambda: None)
    def test_agregar_evento(self):
        with patch("builtins.input", side_effect=[
            "Cumpleaños",        # tipo
            "Juan Perez",        # nombre
            "123456",            # carnet
            "Av. Bolivia",       # direccion
            "50",                # garantia
            "200",               # total
            "2025-12-10",        # fecha
            "18:00",             # hora_fin
            "s"                  # decoracion
        ]):
            with patch("tui.agregar_evento") as mock_agregar:
                tui.agregar_evento_tui()
                mock_agregar.assert_called_once_with(
                    "Cumpleaños",
                    "Juan Perez",
                    "123456",
                    "Av. Bolivia",
                    50.0,
                    200.0,
                    "2025-12-10",
                    "18:00",
                    True
                )

    @patch("tui.pause", lambda: None)
    @patch("tui.clear_screen", lambda: None)
    def test_listar_eventos(self):
        evento1 = FakeEvento(1, "Tipo1", "A", "111", "Dir1", 10, 100,
                             "2024-01-01", "10:00", False)
        evento2 = FakeEvento(2, "Tipo2", "B", "222", "Dir2", 20, 200,
                             "2024-01-02", "12:00", True)

        with patch("tui.listar_eventos", return_value=[evento1, evento2]):
            with patch("builtins.print") as mock_print:
                tui.listar_eventos_tui()
                self.assertTrue(mock_print.called)

    @patch("tui.pause", lambda: None)
    @patch("tui.clear_screen", lambda: None)
    def test_modificar_evento(self):
        # mostrar eventos primero
        evento = FakeEvento(1, "Tipo", "Nombre", "111", "Dir",
                            10, 100, "2024-01-01", "08:00", False)

        with patch("tui.listar_eventos", return_value=[evento]):
            with patch("builtins.input", side_effect=[
                "1",                # id
                "NuevoTipo",        # tipo
                "NuevoNombre",      # nombre
                "999",              # carnet
                "NuevaDir",         # dir
                "30",               # garantia
                "400",              # total
                "2024-02-01",       # fecha
                "09:30",            # hora fin
                "s"                 # decoracion
            ]):
                with patch("tui.modificar_evento") as mock_mod:
                    mock_mod.return_value = True
                    tui.modificar_evento_tui()

                    mock_mod.assert_called_once()
                    args, kwargs = mock_mod.call_args
                    self.assertEqual(args[0], 1)  # ID correcto
                    self.assertEqual(kwargs["tipo"], "NuevoTipo")
                    self.assertEqual(kwargs["nombre"], "NuevoNombre")
                    self.assertEqual(kwargs["carnet"], "999")
                    self.assertEqual(kwargs["direccion_domicilio"], "NuevaDir")
                    self.assertEqual(kwargs["monto_garantia"], 30.0)
                    self.assertEqual(kwargs["monto_total"], 400.0)

    @patch("tui.pause", lambda: None)
    @patch("tui.clear_screen", lambda: None)
    def test_eliminar_evento(self):
        evento = FakeEvento(1, "Tipo", "Nombre", "111", "Dir",
                            10, 100, "2024-01-01", "08:00", False)

        with patch("tui.listar_eventos", return_value=[evento]):
            with patch("builtins.input", side_effect=["1"]):
                with patch("tui.eliminar_evento") as mock_elim:
                    mock_elim.return_value = True
                    tui.eliminar_evento_tui()
                    mock_elim.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()


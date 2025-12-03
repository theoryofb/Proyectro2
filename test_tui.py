import unittest
from unittest.mock import patch
from tui import agregar_evento_tui, listar_eventos_tui, modificar_evento_tui, eliminar_evento_tui
from database import agregar_evento, listar_eventos, modificar_evento, eliminar_evento

class TestTUI(unittest.TestCase):

    @patch('builtins.input', return_value='Evento de prueba')
    def test_agregar_evento(self, mock_input):
        # Simula la entrada de usuario para agregar evento
        with patch('database.agregar_evento') as mock_agregar_evento:
            agregar_evento_tui()
            mock_agregar_evento.assert_called_with(
                'Evento de prueba', 'Evento de prueba', '12345678', 'Calle Falsa 123', 100.0, 150.0, '2023-12-01', '12:00', False
            )

    @patch('builtins.input', side_effect=['1'])
    def test_listar_eventos(self, mock_input):
        # Simula el comportamiento de listar eventos
        eventos = [
            {'id': 1, 'nombre': 'Evento 1', 'dia': '2023-12-01', 'hora': '10:00'},
            {'id': 2, 'nombre': 'Evento 2', 'dia': '2023-12-02', 'hora': '12:00'}
        ]
        
        with patch('database.listar_eventos', return_value=eventos):
            with patch('builtins.print') as mock_print:
                listar_eventos_tui()
                mock_print.assert_called_with(eventos)

    @patch('builtins.input', side_effect=['1', 'Nuevo Evento', '2023-12-02'])
    def test_modificar_evento(self, mock_input):
        # Simula modificar un evento existente
        with patch('database.modificar_evento') as mock_modificar_evento:
            modificar_evento_tui()
            mock_modificar_evento.assert_called_with(1, nombre='Nuevo Evento', dia='2023-12-02')

    @patch('builtins.input', side_effect=['1'])
    def test_eliminar_evento(self, mock_input):
        # Simula eliminar un evento
        with patch('database.eliminar_evento') as mock_eliminar_evento:
            eliminar_evento_tui()
            mock_eliminar_evento.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()


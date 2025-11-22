# calculator_app.py

import sys
# Importamos la librería PySide6 para la interfaz gráfica
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QApplication
)
from PySide6.QtCore import Qt
# Importamos nuestra capa de comunicación con el Kernel
# NOTA: Este archivo debe existir en la misma ruta o en el PYTHONPATH
try:
    from pyos_apis import PyOS_API
except ImportError:
    # Esto ocurre si se ejecuta fuera del entorno PyOS, solo para pruebas locales
    class PyOS_API:
        @staticmethod
        def sys_allocate_ram(bytes_size): return 0xCA1CC0DE
        @staticmethod
        def launch_calculator(): pass
    print("ADVERTENCIA: pyos_apis.py no encontrado. Ejecutando en modo de prueba.")


class CalculatorApp(QWidget):
    """Interfaz de la Calculadora de PyOS, implementada con PySide6."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PyOS Calculator")
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet(self.get_style()) 
        
        # 1. Solicitud de Recurso al Kernel (Delegación de RAM)
        # Esto simula una aplicación pidiendo memoria para su Heap.
        self.mem_address = PyOS_API.sys_allocate_ram(1024 * 512) # 512 KB
        print(f"CALCULATOR: Memoria de 512KB asignada por el Kernel en 0x{self.mem_address:X}")

        self.full_layout = QVBoxLayout()
        self.setLayout(self.full_layout)

        # Configuración de la Pantalla de Resultados
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(50)
        self.display.setText("0")
        self.full_layout.addWidget(self.display)

        # Configuración de los Botones
        self.buttons_layout = QGridLayout()
        self.full_layout.addLayout(self.buttons_layout)

        self.buttons = [
            ('C', 0, 0, 1, 1, self.clear_display), ('/', 0, 3, 1, 1, self.op_clicked),
            ('7', 1, 0, 1, 1, self.num_clicked), ('8', 1, 1, 1, 1, self.num_clicked),
            ('9', 1, 2, 1, 1, self.num_clicked), ('*', 1, 3, 1, 1, self.op_clicked),
            ('4', 2, 0, 1, 1, self.num_clicked), ('5', 2, 1, 1, 1, self.num_clicked),
            ('6', 2, 2, 1, 1, self.num_clicked), ('-', 2, 3, 1, 1, self.op_clicked),
            ('1', 3, 0, 1, 1, self.num_clicked), ('2', 3, 1, 1, 1, self.num_clicked),
            ('3', 3, 2, 1, 1, self.num_clicked), ('+', 3, 3, 1, 1, self.op_clicked),
            ('0', 4, 0, 1, 2, self.num_clicked), ('.', 4, 2, 1, 1, self.op_clicked),
            ('=', 4, 3, 1, 1, self.calculate),
        ]

        self.create_buttons()
        self.clear_state()

    def create_buttons(self):
        """Genera dinámicamente todos los botones de la calculadora."""
        for btn_text, row, col, row_span, col_span, action in self.buttons:
            button = QPushButton(btn_text)
            # Usamos un lambda para pasar el texto del botón y la acción
            button.clicked.connect(lambda checked, text=btn_text, func=action: func(text))
            self.buttons_layout.addWidget(button, row, col, row_span, col_span)

    def get_style(self):
        """Estilo visual de la Calculadora de PyOS (Dark Mode)."""
        return """
            QWidget { background-color: #2e3436; color: white; }
            QLineEdit { 
                background-color: #1c1f21; 
                color: #00ff00; /* Color "Matrix" */
                font: 24pt "Consolas"; 
                border: 2px solid #0055cc;
            }
            QPushButton { 
                background-color: #555753; 
                color: white; 
                border: 1px solid #333;
                font: 14pt;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #666; }
            QPushButton:pressed { background-color: #444; }
        """
        
    def clear_state(self):
        """Reinicia el estado interno de la calculadora."""
        self.pending_value = None
        self.current_op = None

    def num_clicked(self, number):
        """Maneja la entrada de números."""
        current_text = self.display.text()
        
        # Si la pantalla muestra el resultado de una operación anterior o un error
        if current_text in ("0", "Error"):
             self.display.setText(number)
             
        # Si acabamos de pulsar un operador y estamos esperando el segundo número
        elif self.pending_value is not None and current_text == "0":
            self.display.setText(number)
            
        else:
            self.display.setText(current_text + number)

    def op_clicked(self, op):
        """Maneja la entrada de operadores (+, -, *, /)."""
        if op == 'C':
            self.display.setText("0")
            self.clear_state()
            return
        
        if op == '=':
            self.calculate(op)
            return

        # Si ya hay una operación pendiente, la resolvemos primero
        if self.pending_value is not None and self.current_op is not None:
            self.calculate(None)
        
        try:
            self.pending_value = float(self.display.text())
            self.current_op = op
            self.display.setText("0") # Limpiar pantalla para el siguiente número
        except ValueError:
             self.display.setText("Error")
             self.clear_state()


    def clear_display(self, text):
        """Botón C (Clear)."""
        self.display.setText("0")
        self.clear_state()

    def calculate(self, text):
        """Ejecuta la operación pendiente."""
        if self.pending_value is None or self.current_op is None:
            return

        try:
            current_value = float(self.display.text())
            result = 0
            
            # Evaluación del operador
            if self.current_op == '+':
                result = self.pending_value + current_value
            elif self.current_op == '-':
                result = self.pending_value - current_value
            elif self.current_op == '*':
                result = self.pending_value * current_value
            elif self.current_op == '/':
                if current_value == 0:
                    self.display.setText("Error: Division por cero")
                    return
                result = self.pending_value / current_value

            self.display.setText(str(result))
            self.clear_state()

        except Exception:
            self.display.setText("Error")
            self.clear_state()


if __name__ == '__main__':
    # Esta parte solo se ejecuta si se inicia el script directamente (para testing)
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec())
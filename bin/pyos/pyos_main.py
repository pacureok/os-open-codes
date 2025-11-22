# pyos_main.py (Ejecución de la consola y el Escritorio Shell)
from PySide6.QtWidgets import QApplication
from pyos_apis import PyOS_API
import sys
import desktop # El módulo donde estará su GUI de PyQt (escritorio, taskbar, etc.)
# import terminal_app
# import file_explorer 
# import task_manager

def start_pyos_shell():
    """Inicia el Shell de Escritorio."""
    app = QApplication(sys.argv)
    
    # Inicializar el shell/escritorio
    # desk = desktop.PyOSDesktop(PyOS_API)
    # desk.show()
    
    print("PyOS Shell iniciado.")
    # Ejemplo de uso de la API
    new_pid = PyOS_API.sys_create_process("/PyOS-App/terminal_app.py")
    print(f"Terminal lanzado con PID: {new_pid}")
    
    # sys.exit(app.exec()) # Descomentar para ejecutar la GUI
    
if __name__ == "__main__":
    start_pyos_shell()
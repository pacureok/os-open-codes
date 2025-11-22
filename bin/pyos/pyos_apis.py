# pyos_apis.py
import ctypes
from ctypes.util import find_library
import sys
import os

# --- Cargar la Librería C++ Core ---
try:
    if sys.platform.startswith('linux'):
        LIB_NAME = 'libpyos_core.so'
    elif sys.platform == 'win32':
        LIB_NAME = 'libpyos_core.dll'
    else:
        LIB_NAME = find_library('pyos_core') 
    
    if not LIB_NAME:
        raise FileNotFoundError(f"Librería C++ ({LIB_NAME}) no encontrada. Fallo del Kernel.")

    PYOS_CORE_LIB = ctypes.CDLL(LIB_NAME)

    # Definir la signatura de las funciones C
    PYOS_CORE_LIB.pyos_create_process.argtypes = [ctypes.c_char_p]
    PYOS_CORE_LIB.pyos_create_process.restype = ctypes.c_int
    
    PYOS_CORE_LIB.pyos_kill_process.argtypes = [ctypes.c_int]
    PYOS_CORE_LIB.pyos_kill_process.restype = ctypes.c_int
    
    PYOS_CORE_LIB.pyos_allocate_ram.argtypes = [ctypes.c_long]
    PYOS_CORE_LIB.pyos_allocate_ram.restype = ctypes.c_long
    
    PYOS_CORE_LIB.pyos_shutdown.argtypes = []
    PYOS_CORE_LIB.pyos_shutdown.restype = ctypes.c_int
    
    PYOS_CORE_LIB.pyos_get_process_list.argtypes = [ctypes.c_void_p]
    PYOS_CORE_LIB.pyos_get_process_list.restype = ctypes.c_int 

except Exception as e:
    print(f"ERROR CRÍTICO (Kernel Panic): No se pudo enlazar la librería C++: {e}")
    sys.exit(1)

# ------------------------------------------------------------------
#  CLASE PRINCIPAL: PYOS_API
# ------------------------------------------------------------------

class PyOS_API:
    """Clase que expone las Syscalls y APIs del SO PyOS."""
    
    # --- API DE BAJO NIVEL (Syscalls Directas) ---
    @staticmethod
    def sys_create_process(path: str) -> int:
        path_bytes = path.encode('utf-8')
        return PYOS_CORE_LIB.pyos_create_process(path_bytes)

    @staticmethod
    def sys_kill_process(pid: int) -> int:
        return PYOS_CORE_LIB.pyos_kill_process(pid)

    @staticmethod
    def sys_allocate_ram(bytes_size: int) -> int:
        return PYOS_CORE_LIB.pyos_allocate_ram(bytes_size)

    @staticmethod
    def sys_power_off() -> int:
        print("APAGADO: Enviando Syscall al Kernel...")
        return PYOS_CORE_LIB.pyos_shutdown()
        
    # --- API DE MEDIO NIVEL (Librerías del Sistema) ---
    @staticmethod
    def read_large_file(path: str, chunk_size: int = 1024 * 1024) -> str:
        mem_address = PyOS_API.sys_allocate_ram(chunk_size)
        print(f"DEBUG: RAM de {chunk_size/1024} KB asignada por Syscall en 0x{mem_address:X}")
        return f"Datos del archivo {path} cargados en memoria kernelizada."

    # --- API DE ALTO NIVEL (Shell y Aplicación) ---
    @staticmethod
    def open_app(app_name: str, app_path: str):
        print(f"LAUNCHER: Intentando lanzar {app_name}...")
        pid = PyOS_API.sys_create_process(app_path)
        if pid > 0:
            print(f"{app_name} lanzado con éxito. PID: {pid}")
        else:
            print(f"FALLO: El Kernel no pudo iniciar {app_name}.")
            
    @staticmethod
    def launch_calculator():
        PyOS_API.open_app("Calculadora", "/PyOS-App/calculator_app.py")

    @staticmethod
    def get_user_home_path() -> str:
        return "/Principal"
// pyos_core.cpp
#include <iostream>
#include <Python.h> // Requiere que la librería de desarrollo de Python esté vinculada

// --- Función Principal del Shell de PyOS ---
int main(int argc, char *argv[]) {
    // 1. Inicializar el intérprete de Python.
    // Esto es el equivalente a arrancar el motor Python.
    Py_Initialize();

    if (!Py_IsInitialized()) {
        std::cerr << "Error: No se pudo inicializar el intérprete de Python." << std::endl;
        return 1;
    }

    std::cout << "PyOS Core: Intérprete de Python inicializado.\n" << std::endl;

    // --- CONFIGURACIÓN DE RUTA ---
    // 2. Asegurar que Python pueda encontrar los archivos .py (su PyOS).
    // Agregamos el directorio actual ('.') al PATH de Python.
    
    // Este código C ejecuta comandos simples de Python.
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("print('DEBUG: Agregando directorio actual (.) al path de Python.')");
    PyRun_SimpleString("sys.path.append(\".\")"); 


    // --- EJECUCIÓN DEL SISTEMA PYOS ---
    // 3. Importar y ejecutar la función principal de 'main.py'.
    
    std::cout << "PyOS Core: Ejecutando el lanzador de PyOS (main.main())...\n" << std::endl;

    // Bloque de código Python que llama a la función principal.
    // Usamos un bloque try-except para manejo básico de errores de Python.
    PyRun_SimpleString(
        "try:\n"
        "    import main\n"
        "    main.main()\n" // Llama a la función principal de su main.py
        "except ImportError:\n"
        "    print('\\nERROR FATAL: No se encontró main.py. Verifique las rutas.')\n"
        "except Exception as e:\n"
        "    print(f'\\nERROR: Fallo crítico en la ejecución de PyOS: {e}')"
    );

    std::cout << "\nPyOS Core: Proceso de PyOS terminado. Realizando limpieza..." << std::endl;

    // 4. Finalizar el intérprete de Python.
    Py_Finalize();
    
    std::cout << "PyOS Core: Apagado completado." << std::endl;
    return 0;
}
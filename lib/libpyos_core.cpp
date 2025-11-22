// libpyos_core.cpp (Compila a libpyos_core.so)
#include "kernel_api.h"
#include <unistd.h> // Para getpid() en un entorno *hosted*

// Variables de estado global (simuladas)
static int next_pid = 100;
// Note: En el código real, esto sería gestionado por el planificador del Kernel.

extern "C" int pyos_create_process(const char* path) {
    std::cout << "[CPP CORE] Proceso iniciado: " << path << " (PID: " << next_pid << ")" << std::endl;
    // La lógica real aquí: fork() y exec() del proceso.
    // Retorna el nuevo PID
    return next_pid++;
}

extern "C" int pyos_kill_process(int pid) {
    std::cout << "[CPP CORE] Señal de terminación enviada a PID: " << pid << std::endl;
    // La lógica real aquí: enviar la señal SIGKILL.
    return 0; // Éxito
}

extern "C" long pyos_allocate_ram(long bytes) {
    std::cout << "[CPP CORE] Solicitando " << bytes / 1024 << " KB de RAM al Kernel." << std::endl;
    // Lógica real: Llamada a la Syscall de asignación de memoria.
    // Retornamos la dirección de memoria virtual (simulada)
    return 0xDEADBEEF + bytes;
}

extern "C" void pyos_get_process_list(std::vector<ProcessInfo>* list_out) {
    // Lógica real: Recorrer la tabla de procesos del Kernel.
    list_out->clear();
    
    // Simulación de procesos para el Administrador de Tareas
    list_out->push_back({1, "PyOS Kernel", 1500, 0.5});
    list_out->push_back({100, "PyOS Shell (Desktop)", 25000, 5.2});
    list_out->push_back({101, "Terminal App", 8000, 1.1});
    list_out->push_back({102, "File Explorer", 12000, 2.5});
    
    // Nota: La conversión de std::vector a una estructura que ctypes pueda leer es compleja 
    // y requeriría una capa intermedia más detallada (o PyBind11).
}
// kernel_api.h
#ifndef KERNEL_API_H
#define KERNEL_API_H

#include <string>
#include <vector>

// --- Estructuras Reales del Kernel (Asumidas) ---
// En el SO real, estas clases serían implementadas por el Kernel C/C++
namespace Kernel {
    class Scheduler {
    public:
        static int create_process_table_entry();
        static void enqueue_process(int pid, void* entry_point);
    };
    class MemoryManager {
    public:
        static long allocate_pages(long bytes);
        static void release_pages(long address);
    };
    class Hardware {
    public:
        static int power_off();
    };
}

// --- Interfaz de API accesible por Python (extern "C") ---
// Estas funciones son llamadas por la librería ctypes de Python

extern "C" {
    // Punto de entrada del Shell C++ llamado por kernel.c
    void launch_pyos_shell();

    // 1. Gestión de Procesos (Llamadas al Scheduler)
    int pyos_create_process(const char* path);
    int pyos_kill_process(int pid);
    
    // 2. Gestión de RAM (Llamadas al MemoryManager)
    long pyos_allocate_ram(long bytes);
    
    // 3. Gestión de Energía (Llamadas a Hardware)
    int pyos_shutdown(); 
    
    // 4. Monitorización (Para el Task Manager)
    int pyos_get_process_list(void* list_out_ptr); // El puntero sería para una estructura C/C++
}

#endif // KERNEL_API_H
// kernel.c
typedef unsigned int uint32_t;
typedef unsigned char uint8_t;

// Dirección de memoria de video (VGA)
volatile uint8_t *vga_buffer = (volatile uint8_t*)0xB8000;
int vga_cursor_pos = 0;

void print_char(char c, uint8_t color) {
    if (c == '\n') {
        vga_cursor_pos = (vga_cursor_pos / 80 + 1) * 80;
    } else {
        vga_buffer[vga_cursor_pos * 2] = (uint8_t)c;
        vga_buffer[vga_cursor_pos * 2 + 1] = color;
        vga_cursor_pos++;
    }
}

void print_string(const char* str) {
    for (int i = 0; str[i] != '\0'; i++) {
        print_char(str[i], 0x07); // Gris claro sobre Negro
    }
}

// Declaración del lanzador del Shell C++
extern "C" void launch_pyos_shell();

// Punto de entrada del Kernel (Llamado desde boot.asm)
extern "C" void kernel_main(uint32_t magic, uint32_t addr) {
    // 1. Limpiar la pantalla
    for (int i = 0; i < 80 * 25 * 2; i += 2) {
        vga_buffer[i] = ' ';
        vga_buffer[i+1] = 0x07; 
    }

    print_string("PyOS 32-bit Kernel v1.0\n");
    print_string("Inicializando: Paging, Scheduler, Drivers...\n");
    
    // --- Lógica del Kernel Real ---
    // Aquí irían las llamadas a:
    // init_paging(); 
    // init_gdt_idt(); 
    // init_fs_driver(); // Cargar driver de archivos para leer la capa de Python
    
    print_string("Lanzando PyOS Shell (C++ Core)...\n");

    // 2. Saltar a la lógica del lanzador del Shell (que iniciará el intérprete de Python/Qt)
    launch_pyos_shell();

    // 3. Bucle infinito del kernel (debe ser alcanzado solo si el Shell falla)
    while (1) {
        // El kernel esperaría eventos (interrupciones) aquí
    }
}
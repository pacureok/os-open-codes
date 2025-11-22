// Definición básica de tipo (32 bits)
typedef unsigned int uint32_t;

// Función para escribir directamente a la memoria de video (VGA)
// La memoria de video comienza en 0xB8000 en modo texto
volatile unsigned char *vga_buffer = (volatile unsigned char*)0xB8000;
int vga_cursor_pos = 0;

void print_char(char c, char color) {
    if (c == '\n') {
        vga_cursor_pos = (vga_cursor_pos / 80 + 1) * 80;
    } else {
        vga_buffer[vga_cursor_pos * 2] = c;
        vga_buffer[vga_cursor_pos * 2 + 1] = color;
        vga_cursor_pos++;
    }
}

void print_string(const char* str) {
    for (int i = 0; str[i] != '\0'; i++) {
        print_char(str[i], 0x07); // 0x07 = Gris claro sobre Negro
    }
}

// Punto de entrada del Kernel (Llamado desde boot.asm)
// Los argumentos son pasados por el bootloader (GRUB)
void kernel_main(uint32_t magic, uint32_t addr) {
    // 1. Limpiar la pantalla
    for (int i = 0; i < 80 * 25 * 2; i += 2) {
        vga_buffer[i] = ' ';
        vga_buffer[i+1] = 0x07; 
    }

    // 2. Imprimir mensaje de arranque
    print_string("PyOS 32-bit Kernel Iniciado.\n");
    print_string("Modo Protegido Activado.\n");
    
    // Aquí es donde su kernel real ejecutaría el código C++ que incrusta Python.
    // print_string("Llamando a PyOS_Core..."); 
    
    // Bucle infinito del kernel
    while (1) {
        // El kernel esperaría eventos (teclado, disco, etc.) aquí
    }
}
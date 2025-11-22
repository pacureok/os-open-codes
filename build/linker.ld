/* Archivo Linker Script: linker.ld */

ENTRY(_start)             /* Definido en boot.asm */
OUTPUT_FORMAT(elf32-i386) /* Especifica la salida como ELF de 32 bits para Intel */

/* Dirección base de memoria para el kernel (comienza después del bootloader) */
BASE_ADDRESS = 0x100000; 

SECTIONS {
    . = BASE_ADDRESS;

    /* Segmento de arranque y código del kernel */
    .text : ALIGN(4K) {
        *(.multiboot)    /* Se asegura de que el encabezado Multiboot esté al inicio */
        *(.text)         /* Coloca todo el código de texto (funciones) aquí */
    }

    /* Segmento de datos inicializados */
    .data : ALIGN(4K) {
        *(.data)
    }

    /* Segmento de datos no inicializados (pila y variables) */
    .bss : ALIGN(4K) {
        *(.bss)
    }
}
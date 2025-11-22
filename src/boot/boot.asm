; Configuración Multiboot para GRUB
MBOOT_HEADER_MAGIC equ 0x1BADB002 ; Número mágico para Multiboot
MBOOT_PAGE_ALIGN   equ 0x00000001 ; Alineación de página (necesario)
MBOOT_MEMORY_INFO  equ 0x00000002 ; Solicitar información de memoria
MBOOT_HEADER_FLAGS equ MBOOT_PAGE_ALIGN | MBOOT_MEMORY_INFO
MBOOT_CHECKSUM     equ -(MBOOT_HEADER_MAGIC + MBOOT_HEADER_FLAGS)

section .multiboot
    align 4
    dd MBOOT_HEADER_MAGIC
    dd MBOOT_HEADER_FLAGS
    dd MBOOT_CHECKSUM

; ------------------------------------------------------------------
; Stack (Pila) del Kernel
section .bss
    align 4096
    stack_bottom:
    resb 4096 * 4  ; Reserva 16KB para la pila
    stack_top:

; ------------------------------------------------------------------
; Punto de Entrada (Salto a 32 bits)
section .text
    global _start
    extern kernel_main ; Función C que llamaremos

_start:
    ; Configurar el puntero de la pila (Stack Pointer)
    mov esp, stack_top
    
    ; El cargador multiboot (GRUB) pone el estado en EAX y la información en EBX
    ; Los pasamos como argumentos a nuestra función C
    push ebx ; Argumento 2: Multiboot info structure
    push eax ; Argumento 1: Estado (Magic number)

    ; Llamar a la función principal del kernel C
    call kernel_main

    ; Si kernel_main regresa, entramos en un bucle infinito (Halt)
    cli         ; Deshabilitar interrupciones
.halt:
    hlt         ; Detener la CPU
    jmp .halt
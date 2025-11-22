; Configuración Multiboot para GRUB
MBOOT_HEADER_MAGIC equ 0x1BADB002
MBOOT_PAGE_ALIGN   equ 0x00000001
MBOOT_MEMORY_INFO  equ 0x00000002
MBOOT_HEADER_FLAGS equ MBOOT_PAGE_ALIGN | MBOOT_MEMORY_INFO
MBOOT_CHECKSUM     equ -(MBOOT_HEADER_MAGIC + MBOOT_HEADER_FLAGS)

section .multiboot
    align 4
    dd MBOOT_HEADER_MAGIC
    dd MBOOT_HEADER_FLAGS
    dd MBOOT_CHECKSUM

; Stack (Pila) del Kernel (Necesario para las funciones C)
section .bss
    align 4096
    stack_bottom:
    resb 4096 * 4  ; Reserva 16KB para la pila
    stack_top:

; Punto de Entrada (Salto a 32 bits y llamada a C)
section .text
    global _start
    extern kernel_main ; Función C que llamaremos

_start:
    ; Configurar el puntero de la pila (Stack Pointer)
    mov esp, stack_top
    
    ; Pasar los argumentos de Multiboot (EAX, EBX)
    push ebx 
    push eax

    ; Llamar a la función principal del kernel C
    call kernel_main

    ; Si kernel_main regresa, el sistema ha fallado: bucle infinito (Halt)
    cli         ; Deshabilitar interrupciones
.halt:
    hlt         ; Detener la CPU
    jmp .halt
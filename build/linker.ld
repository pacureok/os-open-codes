/* Archivo Linker Script: linker.ld */
ENTRY(_start)             
OUTPUT_FORMAT(elf32-i386) 
BASE_ADDRESS = 0x100000; 

SECTIONS {
    . = BASE_ADDRESS;

    .text : ALIGN(4K) {
        *(.multiboot)    
        *(.text)         
    }

    .data : ALIGN(4K) {
        *(.data)
    }

    .bss : ALIGN(4K) {
        *(.bss)
    }
}
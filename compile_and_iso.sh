#!/bin/bash
# --- Configuración de Rutas ---
KERNEL_DIR="./src/kernel"
BOOT_DIR="./src/boot"
APP_DIR="./src/pyos-app"
BUILD_DIR="./build"
ISO_DIR="./iso"
GRUB_CONFIG="${ISO_DIR}/boot/grub/grub.cfg"

# El objetivo del compilador de 32 bits
TARGET=i686-elf

# Crear directorios si no existen
mkdir -p $BUILD_DIR $ISO_DIR/boot/grub $ISO_DIR/PyOS-App

echo "--- 1. Compilando Assembly (Bootloader) ---"
$TARGET-as $BOOT_DIR/boot.asm -o $BUILD_DIR/boot.o

echo "--- 2. Compilando Kernel C ---"
$TARGET-gcc -c $KERNEL_DIR/kernel.c -o $BUILD_DIR/kernel.o -std=gnu99 -ffreestanding -O2 -Wall -Wextra

# --- PASO EXTRA (CONCEPTUAL): Compilación del C++ Core ---
# NOTA: Esta línea DEBE ser adaptada para enlazar con la librería de Python (ej: -lpython3.11).
# Si no has configurado la vinculación a Python en tu cross-compiler, esta línea fallará en el mundo real.
echo "--- 3. Compilando C++ Launcher (pyos_core) ---"
g++ $APP_DIR/pyos_core.cpp -o $BUILD_DIR/pyos_core.o # Usamos el gcc del host para este ejecutable de usuario
# Idealmente, aquí se vincularía con Python:
# $TARGET-gcc $APP_DIR/pyos_core.cpp -o $BUILD_DIR/pyos_core.o ... -lpython3.11

echo "--- 4. Enlazando (Linking) el Kernel Binario ---"
# Enlazar el boot.o y kernel.o usando el linker script
$TARGET-gcc -T $BUILD_DIR/linker.ld -o $BUILD_DIR/kernel.bin -ffreestanding -O2 -nostdlib $BUILD_DIR/boot.o $BUILD_DIR/kernel.o

if [ ! -f "$BUILD_DIR/kernel.bin" ]; then
    echo "ERROR: Falló la creación de kernel.bin. Abortando."
    exit 1
fi

echo "--- 5. Copiando archivos al directorio ISO ---"
# Copiar el kernel binario a la ubicación donde lo buscará GRUB
cp $BUILD_DIR/kernel.bin $ISO_DIR/boot/kernel.bin

# Copiar los archivos de la aplicación (Python/C++) al ISO
cp $APP_DIR/*.py $ISO_DIR/PyOS-App/
cp $BUILD_DIR/pyos_core.o $ISO_DIR/PyOS-App/pyos_core

echo "--- 6. Creando archivo de configuración GRUB ---"
# Crear el grub.cfg (ver el código en el Paso 4)
cat > $GRUB_CONFIG << EOF
set timeout=5
set default=0

menuentry "PyOS Ultimate" {
    multiboot /boot/kernel.bin
    boot
}
EOF

echo "--- 7. Generando el archivo .ISO Final ---"
# Usar grub-mkrescue para crear la imagen ISO booteable
grub-mkrescue -o PyOS.iso $ISO_DIR

echo "--- ¡COMPLETADO! Archivo PyOS.iso creado ---"
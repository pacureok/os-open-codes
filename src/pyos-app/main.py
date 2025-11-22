import tkinter as tk
from tkinter import messagebox
import os
import json
import installer
import pyos_gui as desktop # Importamos la lógica de escritorio con el alias 'desktop'

def main():
    # 1. Crear la ventana principal (Root)
    root = tk.Tk()
    root.geometry("800x600")
    
    try:
        root.iconbitmap("icoos.ico")
    except:
        pass 

    # 2. Iniciar el chequeo de configuración
    check_and_load(root)
    
    # 3. Iniciar el bucle principal
    root.mainloop()

def check_and_load(root):
    """Decide qué pantalla mostrar (Instalador, Bootloader o Escritorio)."""
    
    config_path = "config.json"
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                data = json.load(f)
                
            is_installed = data.get("installed")
            os_style = data.get("os_style")
            
            if not is_installed:
                # Caso 1: Archivo existe pero la instalación no terminó
                installer.run_installer(root, lambda: check_and_load(root))
            elif os_style is None:
                # Caso 2: Instalado, pero el usuario debe elegir el estilo (bootloader)
                show_bootloader(root)
            else:
                # Caso 3: Todo listo, cargar el escritorio
                desktop.launch_desktop(root, os_style)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error de configuración: {e}. Reiniciando instalador.")
            # Reiniciar la instalación si el archivo está corrupto
            installer.run_installer(root, lambda: check_and_load(root))
    else:
        # Caso 4: No existe archivo de configuración, iniciar instalación
        installer.run_installer(root, lambda: check_and_load(root))

def show_bootloader(root):
    """Muestra la pantalla de selección de estilo de PyOS."""
    for w in root.winfo_children(): w.destroy()
    
    root.title("Bienvenido a PyOS")
    root.configure(bg="black")
    root.state('zoomed')

    tk.Label(root, text="Configuración Inicial", font=("Arial", 24), bg="black", fg="white").pack(pady=50)

    def save_and_start(style):
        with open("config.json", "r+") as f:
            data = json.load(f)
            data["os_style"] = style
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            
        desktop.SYSTEM_CONFIG["os_style"] = style
        desktop.save_config()
        
        desktop.launch_desktop(root, style)

    styles = ["Windows", "MacOS", "Linux", "ChromeOS", "Hacker"] 
    for s in styles:
        fg_col = "#00ff00" if s == "Hacker" else "black"
        bg_col = "black" if s == "Hacker" else "#f0f0f0"
        
        tk.Button(root, text=f"Modo {s}", font=("Arial", 12), width=20, fg=fg_col, bg=bg_col,
                  command=lambda st=s: save_and_start(st)).pack(pady=10)

if __name__ == "__main__":
    main()
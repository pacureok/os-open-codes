import tkinter as tk
from tkinter import messagebox
import json
import time

# --- CONFIGURACIÓN DE INSTALACIÓN ---
INSTALL_CONFIG = {
    "language": "Español",
    "partition": "sda1 - 100 GB"
}

# --- FUNCIÓN DE INICIO DEL INSTALADOR ---

def run_installer(root, callback):
    """Inicia el instalador y maneja los pasos."""
    
    for w in root.winfo_children(): w.destroy()
    
    # Usaremos una variable de control para navegar entre pasos
    control_frame = tk.Frame(root, bg="#2d2d2d")
    control_frame.pack(expand=True, fill="both")
    
    current_step = tk.IntVar(value=1)

    def next_step():
        current_step.set(current_step.get() + 1)
        show_step(current_step.get())
        
    def show_step(step):
        # Limpiar el frame de control
        for w in control_frame.winfo_children(): w.destroy()
        
        if step == 1:
            step_language(control_frame, next_step, root)
        elif step == 2:
            step_partitioning(control_frame, next_step, root)
        elif step == 3:
            step_summary_and_install(control_frame, callback, root)
        else:
            callback() 

    show_step(current_step.get())

# --- PASO 1: SELECCIÓN DE IDIOMA ---

def step_language(parent_frame, next_callback, root_window):
    root_window.title("Instalador de PyOS - Paso 1/3: Idioma")
    step_frame = tk.Frame(parent_frame, bg="#2d2d2d")
    step_frame.pack(expand=True)
    
    tk.Label(step_frame, text="1. Selecciona tu Idioma", font=("Arial", 24), fg="white", bg="#2d2d2d").pack(pady=20)
    
    lang_var = tk.StringVar(value=INSTALL_CONFIG["language"])
    
    languages = ["Español", "English", "Français", "Deutsch"]
    
    for lang in languages:
        tk.Radiobutton(step_frame, text=lang, variable=lang_var, value=lang, 
                       font=("Arial", 12), bg="#2d2d2d", fg="white", selectcolor="#2d2d2d").pack(anchor="w", padx=50)
    
    def save_and_continue():
        INSTALL_CONFIG["language"] = lang_var.get()
        next_callback()

    tk.Button(step_frame, text="Siguiente >>", font=("Arial", 12, "bold"), bg="#0078D7", fg="white", command=save_and_continue).pack(pady=30)

# --- PASO 2: ADMINISTRACIÓN DE PARTICIONES (Simulada) ---

def step_partitioning(parent_frame, next_callback, root_window):
    root_window.title("Instalador de PyOS - Paso 2/3: Disco")
    step_frame = tk.Frame(parent_frame, bg="#2d2d2d")
    step_frame.pack(expand=True)
    
    tk.Label(step_frame, text="2. Selecciona Partición de Destino", font=("Arial", 24), fg="white", bg="#2d2d2d").pack(pady=20)
    
    partition_var = tk.StringVar(value=INSTALL_CONFIG["partition"])
    
    disks = [
        ("sda1 - PyOS", 100),
        ("sdb1 - Data", 500),
        ("sdc1 - Backup", 200)
    ]
    
    list_frame = tk.Frame(step_frame, bg="white", bd=1, relief="sunken")
    list_frame.pack(pady=10)

    # Encabezados de la tabla
    tk.Label(list_frame, text="Disco/Partición", width=15, bd=1, relief="ridge", bg="#ccc").grid(row=0, column=0)
    tk.Label(list_frame, text="Tamaño (GB)", width=10, bd=1, relief="ridge", bg="#ccc").grid(row=0, column=1)
    tk.Label(list_frame, text="Uso", width=10, bd=1, relief="ridge", bg="#ccc").grid(row=0, column=2)
    tk.Label(list_frame, text="Sistema Archivos", width=15, bd=1, relief="ridge", bg="#ccc").grid(row=0, column=3)

    for i, (name, size) in enumerate(disks):
        p_name = f"{name} ({size} GB)"
        
        tk.Radiobutton(list_frame, text=p_name, variable=partition_var, value=p_name, 
                       bg="white", command=lambda n=p_name: print(f"Seleccionado: {n}")).grid(row=i+1, column=0, sticky="w")
        
        # Simulación de barra de espacio
        usage_frame = tk.Frame(list_frame, bg="white", width=200, height=20)
        usage_frame.grid(row=i+1, column=1, columnspan=2, padx=5, sticky="w")
        
        # Simulación de uso (e.g., 20% usado)
        used_width = int(200 * 0.2) 
        tk.Label(usage_frame, bg="#0078D7", width=int(used_width/8), height=1).pack(side="left")
        tk.Label(usage_frame, bg="#eeeeee", width=int((200-used_width)/8), height=1).pack(side="left")
        
        tk.Label(list_frame, text="ext4", bg="white").grid(row=i+1, column=3)

    # Botones de administración simulados
    btn_frame = tk.Frame(step_frame, bg="#2d2d2d")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Nuevo (Simulado)", command=lambda: messagebox.showinfo("Simulación", "Creación de partición simulada.")).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Formatear (Simulado)", command=lambda: messagebox.showwarning("Simulación", "Formato simulado.")).pack(side="left", padx=5)

    def save_and_continue():
        INSTALL_CONFIG["partition"] = partition_var.get()
        next_callback()

    tk.Button(step_frame, text="Siguiente >>", font=("Arial", 12, "bold"), bg="#0078D7", fg="white", command=save_and_continue).pack(pady=30)

# --- PASO 3: RESUMEN E INSTALACIÓN FINAL ---

def step_summary_and_install(parent_frame, final_callback, root_window):
    root_window.title("Instalador de PyOS - Paso 3/3: Finalizar")
    step_frame = tk.Frame(parent_frame, bg="#2d2d2d")
    step_frame.pack(expand=True)

    tk.Label(step_frame, text="3. Resumen y Confirmación", font=("Arial", 24), fg="white", bg="#2d2d2d").pack(pady=20)

    summary_frame = tk.Frame(step_frame, bg="#1a1a1a", padx=20, pady=20)
    summary_frame.pack(pady=10, fill="x", padx=100)

    tk.Label(summary_frame, text=f"Idioma: {INSTALL_CONFIG['language']}", fg="white", bg="#1a1a1a", anchor="w").pack(fill="x")
    tk.Label(summary_frame, text=f"Partición: {INSTALL_CONFIG['partition']}", fg="white", bg="#1a1a1a", anchor="w").pack(fill="x")
    
    progress_var = tk.StringVar(value="Esperando confirmación...")
    progress_label = tk.Label(step_frame, textvariable=progress_var, font=("Arial", 12), fg="white", bg="#2d2d2d")
    progress_label.pack(pady=10)
    
    install_btn = tk.Button(step_frame, text="Instalar PyOS Ahora", font=("Arial", 14, "bold"), bg="#00aa00", fg="white")
    install_btn.pack(pady=20)
    
    def simulate_install(step=0):
        messages = [
            " [1/5] Inicializando sistema de archivos...",
            " [2/5] Copiando archivos de PyOS...",
            " [3/5] Configurando el entorno Tkinter...",
            " [4/5] Guardando preferencias de usuario...",
            " [5/5] Finalizando la instalación y bootloader."
        ]
        
        if step < len(messages):
            progress_var.set(messages[step])
            install_btn.configure(text="INSTALANDO...", state="disabled")
            parent_frame.after(1000, simulate_install, step + 1)
        else:
            progress_var.set("¡Instalación Completa! Iniciando PyOS...")
            
            # Guardar el estado final
            with open("config.json", "w") as f:
                json.dump({"installed": True, "os_style": None}, f, indent=4)
                
            parent_frame.after(2000, final_callback) 

    install_btn.configure(command=simulate_install)
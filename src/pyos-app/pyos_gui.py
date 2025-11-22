import tkinter as tk
from tkinter import messagebox, colorchooser
import json
import os
from PIL import Image, ImageTk 
from calculator import CalculatorApp

# --- CONFIGURACIÓN GLOBAL ---
# Cargar/Definir configuración (Ahora se guarda en sys_config.json)
SYSTEM_CONFIG = {
    "title_bar_color": "#0055cc",
    "show_min": True,
    "show_max": True,
    "transparency": 1.0, 
    "os_style": "Windows"
}
CONFIG_FILE = "sys_config.json"

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            SYSTEM_CONFIG.update(json.load(f))
    except:
        pass

def save_config():
    """Guarda la configuración avanzada del sistema."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(SYSTEM_CONFIG, f, indent=4)

# --- GESTOR DE IMÁGENES y CÓDIGO BÁSICO ---
icon_cache = {}

def cargar_icono(archivo, size=(32, 32)):
    """Carga .ico/.png usando Pillow para compatibilidad y redimensionamiento."""
    try:
        pil_image = Image.open(archivo)
        pil_image = pil_image.resize(size, Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)
        icon_cache[archivo + str(size)] = tk_image 
        return tk_image
    except:
        return None

# --- CLASE: TERMINAL SIMULADA ---
class TerminalApp:
    def __init__(self, parent_frame):
        # ... (El código de la TerminalApp es el mismo que el anterior, sin cambios)
        self.frame = tk.Frame(parent_frame, bg="black")
        self.frame.pack(fill="both", expand=True)
        
        self.text_area = tk.Text(self.frame, bg="black", fg="#00ff00", font=("Consolas", 10), insertbackground="white")
        self.text_area.pack(fill="both", expand=True)
        
        self.prompt = "user@pyos:~$ "
        self.text_area.insert(tk.END, "Bienvenido a PyOS Terminal v1.0\nEscribe 'help' para ver comandos.\n\n" + self.prompt)
        
        self.text_area.bind("<Return>", self.process_command)
        self.text_area.bind("<Key>", self.prevent_delete_prompt)

    def prevent_delete_prompt(self, event):
        # Lógica básica para evitar borrar el prompt
        if self.text_area.index(tk.INSERT).split('.')[1] < str(len(self.prompt)):
             return "break" # Evita que se mueva el cursor antes del prompt (lógica simple)
        pass 

    def process_command(self, event):
        full_text = self.text_area.get("1.0", tk.END).strip()
        lines = full_text.split("\n")
        last_line = lines[-1]
        
        if last_line.startswith(self.prompt):
            command = last_line.replace(self.prompt, "").strip()
            self.execute(command)
        
        return "break"

    def execute(self, cmd):
        response = ""
        if cmd == "help":
            response = "\nComandos disponibles:\n  help   - Muestra ayuda\n  ver    - Versión de PyOS\n  ls     - Listar archivos (simulado)\n  clear  - Limpiar pantalla\n  exit   - Cerrar terminal (simulado)"
        elif cmd == "ver":
            response = "\nPyOS Kernel v3.12"
        elif cmd == "ls":
            response = "\nDesktop/  Documents/  System32/  config.json  main.py"
        elif cmd == "clear":
            self.text_area.delete("1.0", tk.END)
            response = "" 
        elif cmd == "":
            response = ""
        else:
            response = f"\nComando no encontrado: {cmd}"
        
        if cmd != "clear":
            self.text_area.insert(tk.END, response + "\n" + self.prompt)
        else:
            self.text_area.insert(tk.END, self.prompt)
            
        self.text_area.see(tk.END)

# --- CLASE VENTANA INTERNA (Mejorada) ---
class InternalWindow:
    def __init__(self, desktop, taskbar_manager, title, width, height, icon_file):
        self.desktop = desktop
        self.taskbar_manager = taskbar_manager
        
        # Crear frame de ventana
        self.win_frame = tk.Frame(desktop, bd=1, relief="flat", bg="#444")
        self.win_frame.place(x=100, y=100, width=width, height=height)
        self.win_frame.lift() # Asegurar que esté al frente
        
        # --- BARRA DE TÍTULO ---
        bar_color = SYSTEM_CONFIG["title_bar_color"]
        fg_color = "white" if bar_color != "white" else "black"
        
        self.title_bar = tk.Frame(self.win_frame, bg=bar_color, height=30)
        self.title_bar.pack(fill="x", side="top")
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_bar.bind("<Button-1>", self.lift_window, add="+")

        # Icono y Título
        ico_small = cargar_icono(icon_file, size=(16, 16))
        if ico_small:
            lbl_ico = tk.Label(self.title_bar, image=ico_small, bg=bar_color)
            lbl_ico.pack(side="left", padx=5)
            lbl_ico.image = ico_small 

        tk.Label(self.title_bar, text=title, bg=bar_color, fg=fg_color, font=("Segoe UI", 9, "bold")).pack(side="left")
        
        # --- BOTONES DE CONTROL (Configurables) ---
        tk.Button(self.title_bar, text="✕", bg="#ff4444", fg="white", bd=0, width=3, command=self.close).pack(side="right", padx=2)
        
        if SYSTEM_CONFIG["show_max"]:
            tk.Button(self.title_bar, text="⬜", bg=bar_color, fg=fg_color, bd=0, width=3, command=self.toggle_maximize).pack(side="right")

        if SYSTEM_CONFIG["show_min"]:
            tk.Button(self.title_bar, text="_", bg=bar_color, fg=fg_color, bd=0, width=3, command=self.toggle_minimize).pack(side="right")
        
        self.content_area = tk.Frame(self.win_frame, bg="#f0f0f0")
        self.content_area.pack(fill="both", expand=True)
        
        self.task_btn = self.taskbar_manager.add_task(title, icon_file, self.toggle_minimize)
        
        self.is_maximized = False
        self.pre_max_geo = {}

    # (Funciones de movimiento, minimizado, maximizado y cerrado se mantienen igual)
    def start_move(self, event):
        self._drag_x = event.x
        self._drag_y = event.y
        self.lift_window(None)

    def do_move(self, event):
        if not self.is_maximized:
            x = self.win_frame.winfo_x() + (event.x - self._drag_x)
            y = self.win_frame.winfo_y() + (event.y - self._drag_y)
            self.win_frame.place(x=x, y=y)

    def lift_window(self, event):
        self.win_frame.lift()

    def toggle_minimize(self):
        if self.win_frame.winfo_viewable():
            self.win_frame.place_forget()
        else:
            self.win_frame.place(x=self.win_frame.winfo_x(), y=self.win_frame.winfo_y())
            self.win_frame.lift()

    def toggle_maximize(self):
        if not self.is_maximized:
            # Guardar posición
            self.pre_max_geo = {
                "x": self.win_frame.winfo_x(), 
                "y": self.win_frame.winfo_y(),
                "w": self.win_frame.winfo_width(),
                "h": self.win_frame.winfo_height()
            }
            # Maximizar
            self.win_frame.place(x=0, y=0, width=self.desktop.winfo_width(), height=self.desktop.winfo_height())
            self.is_maximized = True
        else:
            # Restaurar
            g = self.pre_max_geo
            self.win_frame.place(x=g["x"], y=g["y"], width=g["w"], height=g["h"])
            self.is_maximized = False

    def close(self):
        self.win_frame.destroy()
        self.taskbar_manager.remove_task(self.task_btn)

# --- CLASE MENÚ DE INICIO (Animado) ---
class StartMenu:
    def __init__(self, desktop_frame, launch_commands):
        self.desktop_frame = desktop_frame
        self.launch_commands = launch_commands
        self.is_open = False
        
        # Frame del menú (inicialmente oculto)
        self.menu_frame = tk.Frame(desktop_frame, bg="#202020", width=250, height=400, bd=1, relief="raised")
        self.menu_frame.place(x=0, y=desktop_frame.winfo_height() - 40, anchor="sw")

        self.populate_menu()

    def populate_menu(self):
        """Llena el menú con botones de aplicaciones."""
        tk.Label(self.menu_frame, text="PyOS", bg="#202020", fg="white", font=("Segoe UI", 14, "bold")).pack(pady=10, padx=10, anchor="w")
        
        apps_frame = tk.Frame(self.menu_frame, bg="#202020")
        apps_frame.pack(fill="x", padx=5)

        # Usar los comandos de lanzamiento definidos en launch_desktop
        for name, data in self.launch_commands.items():
            img = cargar_icono(data["icon"], size=(20, 20))
            btn = tk.Button(apps_frame, text=f"  {name}", image=img, compound="left",
                            bg="#202020", fg="white", font=("Segoe UI", 10), bd=0, 
                            activebackground="#404040", anchor="w", command=data["command"])
            btn.image = img
            btn.pack(fill="x", pady=2)

    def toggle_menu(self):
        """Muestra u oculta el menú con una animación simple."""
        if self.is_open:
            self.animate_close(height=400)
        else:
            self.animate_open(height=0)

    def animate_open(self, height):
        """Animación de aparición (de abajo hacia arriba)."""
        if height < 400:
            new_y = self.desktop_frame.winfo_height() - height
            self.menu_frame.place(x=0, y=new_y, anchor="sw")
            self.menu_frame.lift() # Asegurar que esté al frente
            self.desktop_frame.after(10, self.animate_open, height + 40) # Aumenta 40px cada 10ms
        else:
            self.is_open = True

    def animate_close(self, height):
        """Animación de ocultamiento (de arriba hacia abajo)."""
        if height > 0:
            new_y = self.desktop_frame.winfo_height() - (height - 40)
            self.menu_frame.place(x=0, y=new_y, anchor="sw")
            self.desktop_frame.after(10, self.animate_close, height - 40)
        else:
            self.menu_frame.place_forget()
            self.is_open = False


# --- MÁS CLASES Y FUNCIONES (Mantenidas) ---
class DesktopIcon:
    def __init__(self, parent, text, icon_file, x, y, command):
        # ... (Código idéntico al anterior)
        self.frame = tk.Frame(parent, bg=parent["bg"])
        self.frame.place(x=x, y=y)
        img = cargar_icono(icon_file, size=(48, 48))
        if img:
            self.btn = tk.Button(self.frame, text=text, image=img, compound="top",
                                 font=("Segoe UI", 9), bg=parent["bg"], fg="white", 
                                 bd=0, activebackground=parent["bg"], command=command)
        else:
            self.btn = tk.Button(self.frame, text=f"🔲\n{text}", bg="white", command=command)
        self.btn.pack()
        self.btn.bind("<Button-1>", self.start_move)
        self.btn.bind("<B1-Motion>", self.do_move)
    def start_move(self, event): self._drag_data = {"x": event.x, "y": event.y}
    def do_move(self, event):
        new_x = self.frame.winfo_x() + (event.x - self._drag_data["x"])
        new_y = self.frame.winfo_y() + (event.y - self._drag_data["y"])
        self.frame.place(x=new_x, y=new_y)

class TaskbarManager:
    def __init__(self, taskbar_frame):
        self.frame = taskbar_frame
        self.tasks = []
    def add_task(self, title, icon_file, command):
        img = cargar_icono(icon_file, size=(24, 24))
        btn = tk.Button(self.frame, text=f" {title}", image=img, compound="left",
                        command=command, bg="#333", fg="white", relief="flat", padx=10)
        btn.image = img 
        btn.pack(side="left", padx=2, pady=2)
        self.tasks.append(btn)
        return btn
    def remove_task(self, btn):
        btn.destroy()
        if btn in self.tasks: self.tasks.remove(btn)

# --- PANEL DE AJUSTES AVANZADOS (Se mantiene igual) ---
def open_settings(desktop, taskbar_mgr, root_window):
    # ... (Código de open_settings se mantiene igual, usando SYSTEM_CONFIG)
    win = InternalWindow(desktop, taskbar_mgr, "Ajustes del Sistema", 450, 400, "ajustes.ico")
    
    c_frame = tk.Frame(win.content_area, bg="white", padx=20, pady=20)
    c_frame.pack(fill="both", expand=True)
    
    tk.Label(c_frame, text="Personalización", font=("Segoe UI", 14, "bold"), bg="white").pack(anchor="w")
    
    # 1. Color de la Barra
    tk.Label(c_frame, text="Color Barra Apps:", bg="white", font=("bold")).pack(anchor="w", pady=(10,0))
    
    def pick_color():
        color = colorchooser.askcolor()[1]
        if color:
            SYSTEM_CONFIG["title_bar_color"] = color
            save_config()
            messagebox.showinfo("Info", "El color se aplicará a las nuevas ventanas.")

    tk.Button(c_frame, text="Elegir Color", command=pick_color).pack(anchor="w")

    # 2. Botones de Ventana
    tk.Label(c_frame, text="Botones de Ventana:", bg="white", font=("bold")).pack(anchor="w", pady=(10,0))
    
    var_min = tk.BooleanVar(value=SYSTEM_CONFIG["show_min"])
    var_max = tk.BooleanVar(value=SYSTEM_CONFIG["show_max"])
    
    def update_btns():
        SYSTEM_CONFIG["show_min"] = var_min.get()
        SYSTEM_CONFIG["show_max"] = var_max.get()
        save_config()

    tk.Checkbutton(c_frame, text="Mostrar Minimizar", variable=var_min, bg="white", command=update_btns).pack(anchor="w")
    tk.Checkbutton(c_frame, text="Mostrar Maximizar", variable=var_max, bg="white", command=update_btns).pack(anchor="w")

    # 3. Transparencia
    tk.Label(c_frame, text="Transparencia Global:", bg="white", font=("bold")).pack(anchor="w", pady=(10,0))
    
    def update_alpha(val):
        alpha = float(val)
        SYSTEM_CONFIG["transparency"] = alpha
        root_window.attributes('-alpha', alpha) 
        save_config()
        
    scale = tk.Scale(c_frame, from_=0.3, to=1.0, resolution=0.1, orient="horizontal", bg="white", command=update_alpha)
    scale.set(SYSTEM_CONFIG["transparency"])
    scale.pack(fill="x")

    # 4. Reiniciar
    tk.Button(c_frame, text="Reiniciar PyOS", bg="#ff4444", fg="white", command=lambda: root_window.destroy()).pack(pady=20)

# --- FUNCIÓN PRINCIPAL DE LANZAMIENTO DEL ESCRITORIO ---
def launch_desktop(root, os_style):
    for w in root.winfo_children(): w.destroy()
    
    root.attributes('-alpha', SYSTEM_CONFIG["transparency"])
    root.title("PyOS Ultimate")
    root.state('zoomed')
    
    # Intento de icono principal
    try:
        root.iconbitmap("icoos.ico")
    except:
        pass
    
    # --- TEMAS Y MODOS ---
    colors = {
        "Windows":  {"bg": "#0078D7", "bar": "#101010"},
        "MacOS":    {"bg": "#3b5998", "bar": "#f0f0f0"}, 
        "Linux":    {"bg": "#333333", "bar": "#2c3e50"},
        "ChromeOS": {"bg": "#ffffff", "bar": "#202124"},
        "Hacker":   {"bg": "#000000", "bar": "#00ff00"} 
    }
    theme = colors.get(os_style, colors["Windows"])
    
    # Fondo y Animación de inicio
    desktop_frame = tk.Frame(root, bg=theme["bg"])
    
    # Animación simple de entrada (desvanecimiento rápido)
    root.attributes('-alpha', 0.1)
    def fade_in(alpha_val):
        if alpha_val <= SYSTEM_CONFIG["transparency"]:
            root.attributes('-alpha', alpha_val)
            root.after(20, fade_in, alpha_val + 0.1)
    fade_in(0.1)
    
    desktop_frame.pack(fill="both", expand=True)

    # Barra tareas
    taskbar_frame = tk.Frame(root, bg=theme["bar"], height=45)
    taskbar_frame.pack(side="bottom", fill="x")
    
    task_mgr = TaskbarManager(taskbar_frame)

    # --- DEFINICIÓN DE LANZADORES ---
    
    def run_term():
        InternalWindow(desktop_frame, task_mgr, "Terminal", 500, 300, "terminal.ico")
        
    def run_calc():
        win = InternalWindow(desktop_frame, task_mgr, "Calculadora", 300, 400, "calculadora.ico")
        CalculatorApp(win.content_area)

    def run_settings():
        open_settings(desktop_frame, task_mgr, root)
        
    # Mapa de aplicaciones para el Menú de Inicio
    launch_commands = {
        "Calculadora": {"command": run_calc, "icon": "calculadora.ico"},
        "Terminal": {"command": run_term, "icon": "terminal.ico"},
        "Ajustes": {"command": run_settings, "icon": "ajustes.ico"},
        "Explorador": {"command": lambda: messagebox.showinfo("App", "Explorador Simulador"), "icon": "archiapp.ico"},
    }
    
    # Inicializar Menú de Inicio
    start_menu = StartMenu(desktop_frame, launch_commands)
    
    # Botón Inicio
    start_img = cargar_icono("icoos.ico", size=(24, 24))
    if start_img:
        start_btn = tk.Button(taskbar_frame, image=start_img, bg=theme["bar"], bd=0, command=start_menu.toggle_menu)
        start_btn.image = start_img
    else:
        start_btn = tk.Button(taskbar_frame, text="Inicio", bg="#555", fg="white", command=start_menu.toggle_menu)
    start_btn.pack(side="left", padx=10)

    # --- ICONOS ESCRITORIO ---
    DesktopIcon(desktop_frame, "Terminal", "terminal.ico", 50, 50, run_term)
    DesktopIcon(desktop_frame, "Ajustes", "ajustes.ico", 50, 150, run_settings)
    DesktopIcon(desktop_frame, "Calculadora", "calculadora.ico", 150, 50, run_calc)
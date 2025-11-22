import tkinter as tk

class CalculatorApp:
    def __init__(self, parent_frame):
        # La calculadora ahora se dibuja dentro del frame que le pasemos
        self.frame = tk.Frame(parent_frame, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)
        
        self.entry = tk.Entry(self.frame, width=18, font=("Arial", 14), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.on_click(x)
            tk.Button(self.frame, text=button, width=4, height=2, command=action).grid(row=row_val, column=col_val, padx=2, pady=2)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_click(self, char):
        if char == 'C':
            self.entry.delete(0, tk.END)
        elif char == '=':
            try:
                expression = self.entry.get()
                result = eval(expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        else:
            self.entry.insert(tk.END, char)
import tkinter as tk
from tkinter import ttk, filedialog

class GUIManager:
    def __init__(self, root, process_callback):
        self.root = root
        self.root.title("Mini-Lang: Visual Semantic Analyzer Pro")
        self.root.geometry("1450x850") 
        self.process_callback = process_callback

        # --- Colores ---
        self.bg_color = "#f5f6fa"
        self.sidebar_color = "#2f3640"
        self.accent_color = "#44bd32"
        self.error_color = "#e84118"
        self.node_color = "#0097e6"

        self.root.configure(bg=self.bg_color)

        # --- Layout ---
        self.paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg=self.bg_color, borderwidth=0)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # 1. Panel Izquierdo: AST
        self.left_frame = tk.Frame(self.paned, bg="white")
        self.paned.add(self.left_frame, width=650)
        
        tk.Label(self.left_frame, text="RECORRIDO DEL ÁRBOL (AST)", font=("Montserrat", 12, "bold"), 
                 bg="white", fg=self.sidebar_color).pack(pady=10)
        
        self.canvas = tk.Canvas(self.left_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 2. Panel Derecho: Tabla y Auditoría
        self.right_frame = tk.Frame(self.paned, bg=self.bg_color)
        self.paned.add(self.right_frame, width=800)

        # TABLA DE SÍMBOLOS SIMPLIFICADA
        symbol_label_frame = tk.LabelFrame(self.right_frame, text=" Tabla de Símbolos / Identificadores ", 
                                         font=("Arial", 10, "bold"), bg=self.bg_color)
        symbol_label_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Eliminamos DIM y ÁMBITO de las columnas
        cols = ("ID", "Tipo", "Decl", "Refs", "Op")
        self.tree_symbols = ttk.Treeview(symbol_label_frame, columns=cols, show="headings")
        
        self.tree_symbols.heading("ID", text="IDENTIFICADOR")
        self.tree_symbols.heading("Tipo", text="TIPO")
        self.tree_symbols.heading("Decl", text="DECL. EN")
        self.tree_symbols.heading("Refs", text="REFERENCIAS")
        self.tree_symbols.heading("Op", text="OPERADOR") 
        
        self.tree_symbols.column("ID", width=120, anchor=tk.W)
        self.tree_symbols.column("Tipo", width=80, anchor=tk.CENTER)
        self.tree_symbols.column("Decl", width=80, anchor=tk.CENTER)
        self.tree_symbols.column("Refs", width=150, anchor=tk.W)
        self.tree_symbols.column("Op", width=100, anchor=tk.CENTER) 
        
        self.tree_symbols.pack(fill=tk.BOTH, expand=True)

        # Consola de Auditoría
        console_frame = tk.LabelFrame(self.right_frame, text=" Auditoría de Procesamiento ", 
                                     font=("Arial", 10, "bold"), bg=self.bg_color)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.console = tk.Text(console_frame, bg=self.sidebar_color, fg="#dcdde1", 
                               font=("Consolas", 10), state=tk.DISABLED)
        self.console.pack(fill=tk.BOTH, expand=True)

        # --- CONTENEDOR DE BOTONES ---
        button_container = tk.Frame(self.right_frame, bg=self.bg_color)
        button_container.pack(fill=tk.X, padx=10, pady=10)

        self.btn_load = tk.Button(button_container, text="CARGAR JSON Y ANALIZAR", 
                                  command=self.load_file, bg=self.node_color, fg="white",
                                  font=("Arial", 10, "bold"), pady=10)
        self.btn_load.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # NUEVO BOTÓN: LIMPIAR TODO
        self.btn_clear = tk.Button(button_container, text="LIMPIAR PANEL", 
                                   command=self.clear_all, bg="#7f8c8d", fg="white",
                                   font=("Arial", 10, "bold"), pady=10)
        self.btn_clear.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

    # --- FUNCIONES DE ACTUALIZACIÓN ---

    def clear_all(self):
        """Limpia el árbol, la tabla y la consola"""
        self.canvas.delete("all")
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)
        for item in self.tree_symbols.get_children():
            self.tree_symbols.delete(item)
        print("Interfaz reiniciada.")

    def draw_node(self, x, y, text, is_root=False, color=None):
        fill_color = "#273c75" if is_root else (color if color else self.node_color)
        r = 25
        self.canvas.create_oval(x-r+2, y-r+2, x+r+2, y+r+2, fill="#d1d8e0", outline="")
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill_color, outline="white", width=2)
        self.canvas.create_text(x, y, text=text, fill="white", font=("Arial", 8, "bold"), justify=tk.CENTER)
        self.root.update()

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1+25, x2, y2-25, fill="#7f8c8d", width=2, arrow=tk.LAST)
        self.root.update()

    def log(self, message):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, f"> {message}\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        self.root.update()

    def update_symbol_table_visual(self, stack):
        """Versión simplificada de la tabla"""
        for item in self.tree_symbols.get_children():
            self.tree_symbols.delete(item)
        
        # Recorremos la pila de ámbitos
        for scope in stack:
            for name, info in scope.items():
                refs_str = ", ".join(map(str, info['refs']))
                self.tree_symbols.insert("", tk.END, values=(
                    name, 
                    info['type'], 
                    info['decl_line'], 
                    refs_str, 
                    info.get('last_op', 'N/A')
                ))
        self.root.update()

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.clear_all() # Limpiamos antes de empezar un nuevo análisis
            self.process_callback(path)

    def show_final_result(self, message):
        self.log("-" * 40)
        self.log(message.upper())
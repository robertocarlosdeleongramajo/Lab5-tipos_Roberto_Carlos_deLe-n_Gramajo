import tkinter as tk
from tkinter import filedialog, messagebox

class GUIManager:
    def __init__(self, process_callback):
        self.root = tk.Tk()
        self.root.title("Analizador Semántico - Mini-Lang")
        self.root.geometry("800x600")
        self.process_callback = process_callback 

        self._setup_ui()

    def _setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.btn_load = tk.Button(top_frame, text="Cargar JSON Externo", command=self._load_file)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.lbl_path = tk.Label(top_frame, text="Ningún archivo seleccionado", fg="gray")
        self.lbl_path.pack(side=tk.LEFT)

        tk.Label(self.root, text="Tabla de Símbolos Final:").pack()
        self.txt_symbols = tk.Text(self.root, height=10, width=90)
        self.txt_symbols.pack(pady=5)

        tk.Label(self.root, text="Consola de Resultados / Errores:").pack()
        self.txt_errors = tk.Text(self.root, height=15, width=90, fg="red")
        self.txt_errors.pack(pady=5)

    def _load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if file_path:
            self.lbl_path.config(text=file_path, fg="black")
            self.process_callback(file_path)

    def update_results(self, symbols_text, errors_text, success=False):
        self.txt_symbols.delete('1.0', tk.END)
        self.txt_symbols.insert(tk.END, symbols_text)

        self.txt_errors.delete('1.0', tk.END)
        self.txt_errors.insert(tk.END, errors_text)
        
        if success:
            self.txt_errors.config(fg="green")
        else:
            self.txt_errors.config(fg="red")

    def run(self):
        self.root.mainloop()
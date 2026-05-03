import tkinter as tk
import json
from symbol_table import SymbolTable
from type_checker import TypeChecker
from error_handler import ErrorHandler
from json_processor import JSONProcessor
from gui_manager import GUIManager

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # 1. El ErrorHandler debe ser lo primero en existir
        self.error_handler = ErrorHandler()

        # 2. El TypeChecker ahora recibe al error_handler (Arregla el error de tu captura)
        self.type_checker = TypeChecker(self.error_handler)

        # 3. Inicializar el resto de la lógica
        self.symbol_table = SymbolTable()

        # 4. Inicializar la GUI
        self.gui = GUIManager(self.root, self.start_analysis)

        # 5. Inicializar el Procesador con sus 4 dependencias
        self.processor = JSONProcessor(
            self.symbol_table, 
            self.type_checker, 
            self.error_handler, 
            self.gui
        )

    def start_analysis(self, file_path):
        """Función que se dispara al presionar el botón en la GUI"""
        # Limpieza total para un nuevo análisis
        self.symbol_table = SymbolTable() 
        self.error_handler.clear_errors()
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.gui.log("--- Iniciando Nuevo Análisis Semántico ---")
                
                # Ejecutar el procesamiento del JSON
                self.processor.process(data.get("programa", []))
                
                # Verificación final de errores para el mensaje de éxito/fallo
                if self.error_handler.has_errors():
                    self.gui.show_final_result("Compilación con Errores")
                else:
                    self.gui.show_final_result("Compilación Semántica Exitosa")
                    
        except Exception as e:
            self.gui.log(f"ERROR CRÍTICO: {str(e).upper()}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
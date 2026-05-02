import json
from symbol_table import SymbolTable
from type_checker import TypeChecker
from error_handler import ErrorHandler
from json_processor import JSONProcessor
from gui_manager import GUIManager

def start_analysis(file_path):
    errors = ErrorHandler()
    symbols = SymbolTable()
    checker = TypeChecker(errors)
    processor = JSONProcessor(symbols, checker, errors)

    data = processor.load_json(file_path)
    if data:
        processor.analyze(data)

    symbols_display = "--- TABLA DE SÍMBOLOS FINAL ---\n"
    for i, scope in enumerate(symbols.get_all_scopes()):
        symbols_display += f"Ámbito {i}: {json.dumps(scope, indent=4)}\n"

    report = errors.get_report()
    is_success = not errors.has_errors()

    gui.update_results(symbols_display, report, success=is_success)

if __name__ == "__main__":
    gui = GUIManager(start_analysis)
    print("Analizador Semántico Mini-Lang iniciado...")
    gui.run()
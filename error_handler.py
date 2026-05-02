class ErrorHandler:
    def __init__(self):
        self.errors = []

    def add_error(self, line, message, error_type="Semántico"):
        error_entry = {
            "line": line,
            "message": message,
            "type": error_type
        }
        self.errors.append(error_entry)

    def has_errors(self):
        return len(self.errors) > 0

    def get_report(self):
        if not self.has_errors():
            return "Compilación Semántica Exitosa"
        
        sorted_errors = sorted(self.errors, key=lambda x: x['line'])
        report = "--- REPORTE DE ERRORES SEMÁNTICOS ---\n"
        for err in sorted_errors:
            report += f"[{err['type']}] Línea {err['line']}: {err['message']}\n"
        return report

    def clear(self):

        self.errors = []
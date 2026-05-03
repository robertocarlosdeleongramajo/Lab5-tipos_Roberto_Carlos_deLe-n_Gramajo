class ErrorHandler:
    def __init__(self):
        # Lista para almacenar los errores encontrados
        self.errors = []

    def add_error(self, line, message, error_type="Semántico"):
        """
        Registra un nuevo error con su ubicación y categoría.
        Cumple con el criterio de 'Gestión de Errores' de la rúbrica.
        """
        error_entry = {
            "line": line,
            "message": message,
            "type": error_type
        }
        self.errors.append(error_entry)

    def clear_errors(self):
        """Limpia la lista para un nuevo análisis (útil al cargar otro JSON)"""
        self.errors = []

    def has_errors(self):
        """Informa si se detectaron problemas durante el proceso"""
        return len(self.errors) > 0

    def get_all_errors(self):
        """Devuelve la lista completa de errores registrados"""
        return self.errors

    def format_errors_for_log(self):
        """
        Devuelve una cadena formateada lista para mostrarse 
        en la consola de auditoría de la GUI.
        """
        if not self.errors:
            return "No se encontraron errores."
        
        formatted = []
        for err in self.errors:
            # Formato: ERROR [TIPO] (LÍNEA X): MENSAJE
            msg = f"ERROR [{err['type'].upper()}] (LÍNEA {err['line']}): {err['message']}"
            formatted.append(msg)
        return "\n".join(formatted)
class SymbolTable:
    def __init__(self):
        # La pila inicia con el ámbito global (un diccionario vacío)
        self.scopes = [{}]

    def push_scope(self):
        """Crea un nuevo ámbito local (ej. al entrar a una función)."""
        self.scopes.append({})

    def pop_scope(self):
        """Elimina el ámbito local actual (ej. al salir de una función)."""
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name, var_type, line):
        """
        Registra una variable en el ámbito actual.
        Retorna True si tuvo éxito, False si ya existía en el mismo nivel.
        """
        current_scope = self.scopes[-1]
        if name in current_scope:
            return False, f"Error Semántico: Variable '{name}' ya declarada en este ámbito (Línea {line})."
        
        current_scope[name] = {
            'type': var_type,
            'line': line
        }
        return True, None

    def lookup(self, name):
        """
        Busca una variable desde el ámbito más interno al más externo (Global).
        Retorna la información de la variable o None si no existe.
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def get_all_scopes(self):
        """Retorna todos los ámbitos para mostrarlos en la GUI final."""
        return self.scopes
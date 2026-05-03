class SymbolTable:
    def __init__(self):
        # La pila de ámbitos inicia con el ámbito global
        self.stack = [{}]

    def push_scope(self):
        """Crea un nuevo nivel de ámbito al entrar en un bloque (IF/WHILE)"""
        self.stack.append({})
        return len(self.stack) - 1

    def pop_scope(self):
        """Elimina el ámbito actual al salir de un bloque"""
        if len(self.stack) > 1:
            return self.stack.pop()
        return {}

    def declare(self, name, datatype, line, dim=0):
        """
        Registra una variable en el ámbito actual.
        Hemos eliminado 'level' y 'dim' del diccionario interno para mayor limpieza.
        """
        current_scope = self.stack[-1]
        
        if name in current_scope:
            return False, f"Error: La variable '{name}' ya existe en este nivel."
        
        # Guardamos solo lo necesario para la tabla visual simplificada
        current_scope[name] = {
            'type': datatype,
            'decl_line': line,
            'refs': [line],
            'last_op': 'N/A'
        }
        return True, f"Variable '{name}' ({datatype}) registrada."

    def lookup(self, name, line_usage=None, operator=None):
        """Busca la variable en la pila (del ámbito más cercano al global)"""
        for scope in reversed(self.stack):
            if name in scope:
                # Actualiza referencias si se usa en una nueva línea
                if line_usage and line_usage not in scope[name]['refs']:
                    scope[name]['refs'].append(line_usage)
                
                # Actualiza el operador para la columna 'OPERADOR'
                if operator:
                    scope[name]['last_op'] = operator
                    
                return scope[name]
        return None

    def get_full_stack(self):
        """Retorna toda la pila para la actualización visual del GUI"""
        return self.stack
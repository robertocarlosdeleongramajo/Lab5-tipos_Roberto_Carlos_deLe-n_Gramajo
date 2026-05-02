class SymbolTable:
    def __init__(self):

        self.scopes = [{}]

    def push_scope(self):

        self.scopes.append({})

    def pop_scope(self):

        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name, var_type, line):

        current_scope = self.scopes[-1]
        if name in current_scope:
            return False, f"Error Semántico: Variable '{name}' ya declarada en este ámbito (Línea {line})."
        
        current_scope[name] = {
            'type': var_type,
            'line': line
        }
        return True, None

    def lookup(self, name):

        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def get_all_scopes(self):

        return self.scopes
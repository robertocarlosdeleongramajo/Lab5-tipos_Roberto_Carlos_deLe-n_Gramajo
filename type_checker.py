class TypeChecker:
    def __init__(self, error_handler):
        # Ahora recibe el manejador para reportar errores directamente
        self.error_handler = error_handler
        
        # Matriz de reglas basada en tus tablas (image_7866bc.png y image_77f67b.png)
        # Formato: (Tipo A, Tipo B, Operador) -> Tipo Resultante
        self.rules = {
            ('int', 'int', '+'): 'int',
            ('int', 'int', '-'): 'int',
            ('int', 'int', '*'): 'int',
            ('int', 'int', '/'): 'float', # La división suele promocionar
            
            # Promociones (image_77f67b.png)
            ('int', 'float', '+'): 'float',
            ('float', 'int', '+'): 'float',
            ('int', 'float', '*'): 'float',
            ('float', 'int', '*'): 'float',
            
            # Comparaciones (image_7866bc.png)
            ('int', 'int', '<'): 'bool',
            ('int', 'int', '>'): 'bool',
            ('int', 'int', '=='): 'bool',
            
            # Lógicos
            ('bool', 'bool', '&&'): 'bool',
            ('bool', 'bool', '||'): 'bool'
        }

    def check_assignment(self, target_type, value_type, line):
        """Valida si el valor puede guardarse en la variable (image_77f69d.png)"""
        if target_type == value_type:
            return True, f"Asignación válida: {target_type}."
        
        # Caso especial de promoción: de int a float es seguro
        if target_type == 'float' and value_type == 'int':
            return True, "Promoción implícita: int -> float (Seguro)."
        
        # Si no coinciden y no hay promoción, es un error semántico
        msg = f"ERROR DE TIPOS: No se puede asignar '{value_type}' a una variable '{target_type}'"
        self.error_handler.add_error(line, msg, "Semántico")
        return False, msg

    def validate_control_condition(self, cond_type, node_type, line):
        """
        Verifica que IF/WHILE reciban un booleano (image_785416.png)
        """
        if cond_type != 'bool':
            msg = f"ERROR [FLUJO]: TIPO NO BOOLEANO EN {node_type}: SE ESPERABA 'BOOL' PERO SE RECIBIÓ '{cond_type}'"
            self.error_handler.add_error(line, msg, "Flujo")
            return False
        return True
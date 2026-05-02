class TypeChecker:
    def __init__(self, error_handler):
        self.error_handler = error_handler
        # Definimos la matriz de compatibilidad para operaciones aritméticas
        # Formato: (tipo1, operador, tipo2) -> tipo_resultante
        self.compatibility_matrix = {
            ('int', '+', 'int'): 'int',
            ('int', '+', 'float'): 'float',
            ('float', '+', 'int'): 'float',
            ('float', '+', 'float'): 'float',
            ('int', '-', 'int'): 'int',
            ('int', '*', 'int'): 'int',
            ('int', '/', 'int'): 'float', # La división suele dar float
        }

    def check_assignment(self, target_type, value_type, line):
        """Valida si se puede asignar un valor a una variable."""
        if target_type != value_type:
            # Regla especial: permitimos asignar int a una variable float
            if target_type == 'float' and value_type == 'int':
                return True
            
            self.error_handler.add_error(
                line, 
                f"Incompatibilidad de tipos: No se puede asignar {value_type} a una variable {target_type}."
            )
            return False
        return True

    def check_binary_operation(self, left_type, operator, right_type, line):
        """Valida operaciones como suma, resta, etc."""
        result = self.compatibility_matrix.get((left_type, operator, right_type))
        
        if not result:
            self.error_handler.add_error(
                line, 
                f"Operación no válida: {left_type} {operator} {right_type} no está permitido en Mini-Lang."
            )
            return 'error'
        
        return result

    def check_condition(self, condition_type, line):
        """Valida que los IF y WHILE tengan una expresión booleana."""
        if condition_type != 'bool':
            self.error_handler.add_error(
                line, 
                f"Error de control: La condición debe ser bool, se recibió {condition_type}."
            )
            return False
        return True
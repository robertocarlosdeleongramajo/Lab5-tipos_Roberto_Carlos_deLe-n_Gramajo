import time

class JSONProcessor:
    def __init__(self, symbol_table, type_checker, error_handler, gui):
        self.symbol_table = symbol_table
        self.type_checker = type_checker
        self.error_handler = error_handler
        self.gui = gui

    def process(self, instructions, parent_x=None, parent_y=None, level=0):
        """
        Recorre el JSON y dibuja un AST centrado y contenido dentro del panel.
        """
        # --- AJUSTES DINÁMICOS DE VISIBILIDAD ---
        # Forzamos la actualización para obtener el ancho real del canvas (panel izquierdo)
        self.gui.root.update_idletasks()
        canvas_width = self.gui.canvas.winfo_width()
        if canvas_width < 100: canvas_width = 650 # Valor de respaldo
        
        # El spread (separación horizontal) se reduce en niveles profundos para no salirse
        # Usamos un multiplicador de 0.8 para dejar márgenes a los lados
        width_spread = (canvas_width * 0.8) / (level + 1) 
        y_distance = 110 # Distancia vertical constante para claridad

        for i, instr in enumerate(instructions):
            tipo = instr.get("type", "unknown").upper()
            linea = instr.get("line", 0)
            op_actual = instr.get("op", "N/A")

            # --- CÁLCULO DE POSICIÓN ---
            if parent_x is None:
                # Nodo Raíz: Siempre centrado horizontalmente
                curr_x = canvas_width / 2 
                curr_y = 60 # Bajamos un poco el inicio para que no pegue con el título
            else:
                # Nodos Hijos: Distribución simétrica respecto al padre
                offset = (i - (len(instructions) - 1) / 2) * width_spread
                curr_x = parent_x + offset
                curr_y = parent_y + y_distance

            # --- SEGURIDAD DE BORDES ---
            # Evita que las burbujas toquen las paredes del panel (mínimo 40px de margen)
            curr_x = max(45, min(curr_x, canvas_width - 45))

            # --- DISEÑO DEL NODO ---
            color = "#2E86C1" # Azul profesional para declaraciones
            if tipo in ["IF", "WHILE"]:
                color = "#8E44AD" # Púrpura para estructuras de control
            
            label = f"{tipo}\nL:{linea}"
            if op_actual != "N/A":
                label = f"{tipo} [{op_actual}]\nL:{linea}"

            # Dibujamos el nodo y la línea conectora
            self.gui.draw_node(curr_x, curr_y, label, is_root=(level == 0), color=color)
            if parent_x is not None:
                self.gui.draw_line(parent_x, parent_y, curr_x, curr_y)
            
            self.gui.log(f"Analizando nodo: {tipo} (Línea {linea})")
            time.sleep(0.05) 

            # --- LÓGICA SEMÁNTICA (Sin DIM ni ÁMBITO visual) ---
            if tipo == "DECLARATION":
                name = instr.get("name")
                dtype = instr.get("datatype")
                success, msg = self.symbol_table.declare(name, dtype, linea)
                if not success:
                    self.error_handler.add_error(linea, msg, "Semántico")
                self.gui.log(f"  -> {msg}")

            elif tipo == "ASSIGNMENT":
                target = instr.get("target")
                val_type = instr.get("value_type")
                var = self.symbol_table.lookup(target, line_usage=linea, operator=op_actual)
                
                if var:
                    res, msg = self.type_checker.check_assignment(var['type'], val_type, linea)
                    self.gui.log(f"  -> {msg}")
                else:
                    self.error_handler.add_error(linea, f"Variable '{target}' no declarada", "Referencia")

            elif tipo in ["IF", "WHILE"]:
                cond_type = instr.get("condition_type", "unknown")
                self.type_checker.validate_control_condition(cond_type, tipo, linea)
                
                self.symbol_table.push_scope()
                if "block" in instr:
                    # Pasamos las nuevas coordenadas para que los hijos cuelguen de aquí
                    self.process(instr["block"], curr_x, curr_y, level + 1)
                self.symbol_table.pop_scope()

            # Refrescamos la tabla simplificada en cada paso
            self.gui.update_symbol_table_visual(self.symbol_table.get_full_stack())
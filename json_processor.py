import json

class JSONProcessor:
    def __init__(self, symbol_table, type_checker, error_handler):
        self.symbol_table = symbol_table
        self.type_checker = type_checker
        self.error_handler = error_handler

    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            self.error_handler.add_error(0, f"No se pudo leer el archivo JSON: {str(e)}", "Sistema")
            return None

    def analyze(self, data):
        if not data:
            return
        for node in data:
            self.visit_node(node)

    def visit_node(self, node):
        node_type = node.get("type")
        line = node.get("line", 0)

        if node_type == "declaration":
            success, msg = self.symbol_table.declare(node["name"], node["datatype"], line)
            if not success:
                self.error_handler.add_error(line, msg)

        elif node_type == "assignment":
            var_info = self.symbol_table.lookup(node["target"])
            if var_info:
                self.type_checker.check_assignment(var_info['type'], node["value_type"], line)
            else:
                self.error_handler.add_error(line, f"Variable '{node['target']}' no declarada.")

        elif node_type == "operation":
            self.type_checker.check_binary_operation(
                node["left_type"], node["operator"], node["right_type"], line
            )
            
        elif node_type == "scope_start":
            self.symbol_table.push_scope()
            
        elif node_type == "scope_end":
            self.symbol_table.pop_scope()
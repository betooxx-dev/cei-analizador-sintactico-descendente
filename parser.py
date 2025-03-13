from grammar import Grammar
from tokenizer import Tokenizer

class Parser:
    def __init__(self):
        self.grammar = Grammar()
        self.tokenizer = Tokenizer()
        self.tokens = []
        self.index = 0
        self.error_message = ""
        self.parse_tree = []
    
    def parse(self, input_text):
        self.tokens = self.tokenizer.tokenize(input_text)
        self.index = 0
        self.error_message = ""
        self.parse_tree = []
        
        for i, token in enumerate(self.tokens):
            if token[0] == 'error':
                self.error_message = f"Error léxico en línea {token[2]}, columna {token[3]}: Carácter no reconocido '{token[1]}'"
                self.parse_tree.append(f"Error: {self.error_message}")
                return False, self.parse_tree
        
        stack = ['$', 'program']
    
        
        while stack[-1] != '$':
            top = stack[-1]
            current_token = self.tokens[self.index]
            current_token_type = current_token[0]

            self.parse_tree.append(f"Pila: {stack}")
            self.parse_tree.append(f"Entrada: {self.tokens[self.index:]}")
            
            if top in self.grammar.terminals:
                if top == current_token_type:
                    self.parse_tree.append(f"Coincidencia: {top} '{current_token[1]}'")
                    stack.pop()
                    self.index += 1
                else:
                    line, column = current_token[2], current_token[3]
                    self.error_message = f"Error de sintaxis en línea {line}, columna {column}: Se esperaba '{top}', se encontró '{current_token_type}' ('{current_token[1]}')"
                    self.parse_tree.append(f"Error: {self.error_message}")
                    return False, self.parse_tree
            elif top == 'ε':
                self.parse_tree.append(f"Aplicar: {top} -> ε")
                stack.pop()
            else:  
                if current_token_type in self.grammar.parsing_table[top] and self.grammar.parsing_table[top][current_token_type] is not None:
                    production_idx = self.grammar.parsing_table[top][current_token_type]
                    production = self.grammar.productions[top][production_idx]
                    
                    self.parse_tree.append(f"Aplicar: {top} -> {' '.join(production)}")
                    
                    stack.pop()

                    for symbol in reversed(production):
                        if symbol != 'ε':
                            stack.append(symbol)
                else:
                    line, column = current_token[2], current_token[3]
                    self.error_message = f"Error de sintaxis en línea {line}, columna {column}: No hay producción para [{top}, {current_token_type}]"
                    self.parse_tree.append(f"Error: {self.error_message}")
                    return False, self.parse_tree
        
        if self.index < len(self.tokens) - 1:
            remaining_tokens = [t[1] for t in self.tokens[self.index:]]
            self.error_message = f"Error de sintaxis: Entrada no consumida por completo. Restante: {remaining_tokens}"
            self.parse_tree.append(f"Error: {self.error_message}")
            return False, self.parse_tree
        
        self.parse_tree.append("¡Análisis sintáctico exitoso!")
        return True, self.parse_tree
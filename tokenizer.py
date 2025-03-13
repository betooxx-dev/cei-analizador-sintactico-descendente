import re

class Tokenizer:
    def __init__(self):
        self.token_patterns = [
            ('comment', r'//.*'), 
            ('comment', r'/\*[\s\S]*?\*/'), 
            ('comment', r'/[^/*].*'),  
            ('int', r'\bint\b'),
            ('float', r'\bfloat\b'),
            ('string', r'\bstring\b'),
            ('if', r'\bif\b'),
            ('else', r'\belse\b'),
            ('while', r'\bwhile\b'),
            ('input', r'\binput\b'),
            ('print', r'\bprint\b'),
            ('identifier', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('real', r'\d+\.\d+'),
            ('integer', r'\d+'),
            ('str_literal', r'"[^"]*"'),
            ('==', r'=='),
            ('!=', r'!='),
            ('<=', r'<='),
            ('>=', r'>='),
            ('<', r'<'),
            ('>', r'>'),
            ('=', r'='),
            (';', r';'),
            ('{', r'{'),
            ('}', r'}'),
            ('(', r'\('),
            (')', r'\)'),
            ('+', r'\+'),
            ('-', r'-'),
            ('*', r'\*'),
            ('/', r'/'),
            ('%', r'%'),
            (':', r':'), 
            ('whitespace', r'\s+')
        ]
        
        self.operators = ['<', '>', '+', '-', '*', '/', '%', '==', '!=', '<=', '>=']
    
    def tokenize(self, input_text):
        tokens = []
        pos = 0
        line = 1
        column = 1
        
        while pos < len(input_text):
            match = None
            for token_type, pattern in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(input_text[pos:])
                if match:
                    token_text = match.group(0)
                    if token_type not in ['whitespace', 'comment']:  
                        tokens.append((token_type, token_text, line, column))

                    newlines = token_text.count('\n')
                    if newlines > 0:
                        line += newlines
                        column = len(token_text) - token_text.rfind('\n')
                    else:
                        column += len(token_text)
                    
                    pos += len(token_text)
                    break
            
            if not match:
                if pos >= len(input_text):
                    break

                error_char = input_text[pos]
                print(f"Error de tokenización en línea {line}, columna {column}: Carácter no reconocido '{error_char}'")
                
                tokens.append(('error', error_char, line, column))
                
                if error_char == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                
                pos += 1
        
        if not any(token[0] == 'error' for token in tokens):
            error_tokens = self._check_operator_spacing(input_text)
            if error_tokens:
                return error_tokens
        
        tokens.append(('$', '$', line, column)) 
        return tokens
    
    def _check_operator_spacing(self, input_text):
        for op in self.operators:
            id_op_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)(' + re.escape(op) + r')'
            
            for match in re.finditer(id_op_pattern, input_text):
                # Verificar que no estemos dentro de un string o comentario
                if self._is_in_string_or_comment(input_text, match.start()):
                    continue
                
                line, col = self._get_line_col(input_text, match.start(2))
                error_message = f"Error: Falta espacio antes del operador '{match.group(2)}'"
                return [('error', error_message, line, col), ('$', '$', line, col+1)]
            
            op_id_pattern = r'(' + re.escape(op) + r')([a-zA-Z_][a-zA-Z0-9_]*)'
            
            for match in re.finditer(op_id_pattern, input_text):
                if self._is_in_string_or_comment(input_text, match.start()):
                    continue
                
                line, col = self._get_line_col(input_text, match.start(1))
                error_message = f"Error: Falta espacio después del operador '{match.group(1)}'"
                return [('error', error_message, line, col), ('$', '$', line, col+1)]
        
        return None
    
    def _is_in_string_or_comment(self, text, pos):
        """Determina si una posición en el texto está dentro de un string o comentario"""
        in_string = False
        string_start = -1
        
        for i in range(pos):
            if text[i] == '"' and (i == 0 or text[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_start = i
                else:
                    in_string = False
            
            if i < pos - 1 and text[i:i+2] == '//' and not in_string:
                line_text = text[i:pos]
                if '\n' not in line_text:
                    return True
            
            if i < pos - 1 and text[i:i+2] == '/*' and not in_string:
                comment_text = text[i:pos]
                if '*/' not in comment_text:
                    return True
        
        return in_string
    
    def _get_line_col(self, text, pos):
        """Calcula la línea y columna para una posición en el texto"""
        line = 1
        col = 1
        for i in range(pos):
            if text[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
        return line, col
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

                if error_char == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                
                pos += 1
        
        tokens.append(('$', '$', line, column)) 
        return tokens
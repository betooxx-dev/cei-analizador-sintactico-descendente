import tkinter as tk
from tkinter import ttk, scrolledtext
import re

# Grammar and Parsing Table Definition
class Grammar:
    def __init__(self):
        # Define terminals and non-terminals
        self.terminals = [
            'int', 'float', 'string', 'identifier', 'if', 'else', 'while',
            'input', 'print', '(', ')', '{', '}', ';', '=', '==', '!=', '<',
            '>', '<=', '>=', '+', '-', '*', '/', '%', 'integer', 'real', 'str_literal', '$'
        ]
        
        self.non_terminals = [
            'program', 'statement_list', 'statement', 'declaration', 'type',
            'assignment', 'if_statement', 'else_part', 'while_statement',
            'input_statement', 'print_statement', 'condition', 'comparison_op',
            'expression', 'expression_prime', 'term', 'term_prime', 'factor'
        ]
        
        # Define productions
        self.productions = {
            'program': [['statement_list']],
            'statement_list': [['statement', 'statement_list'], ['ε']],
            'statement': [['declaration'], ['assignment'], ['if_statement'], 
                         ['while_statement'], ['input_statement'], ['print_statement']],
            'declaration': [['type', 'identifier', ';']],
            'type': [['int'], ['float'], ['string']],
            'assignment': [['identifier', '=', 'expression', ';']],
            'if_statement': [['if', '(', 'condition', ')', '{', 'statement_list', '}', 'else_part']],
            'else_part': [['else', '{', 'statement_list', '}'], ['ε']],
            'while_statement': [['while', '(', 'condition', ')', '{', 'statement_list', '}']],
            'input_statement': [['input', '(', 'identifier', ')', ';']],
            'print_statement': [['print', '(', 'expression', ')', ';']],
            'condition': [['expression', 'comparison_op', 'expression']],
            'comparison_op': [['=='], ['!='], ['<'], ['>'], ['<='], ['>=']],
            'expression': [['term', 'expression_prime']],
            'expression_prime': [['+', 'term', 'expression_prime'], ['-', 'term', 'expression_prime'], ['ε']],
            'term': [['factor', 'term_prime']],
            'term_prime': [['*', 'factor', 'term_prime'], ['/', 'factor', 'term_prime'], ['%', 'factor', 'term_prime'], ['ε']],
            'factor': [['identifier'], ['integer'], ['real'], ['str_literal'], ['(', 'expression', ')']]
        }
        
        # Define the parsing table
        self.parsing_table = self._create_parsing_table()
    
    def _create_parsing_table(self):
        # Initialize an empty parsing table
        table = {}
        for nt in self.non_terminals:
            table[nt] = {}
            for t in self.terminals + ['$']:
                table[nt][t] = None
        
        # Fill in the table based on our grammar
        
        # program -> statement_list
        for t in ['int', 'float', 'string', 'identifier', 'if', 'while', 'input', 'print', '$']:
            table['program'][t] = 0
        
        # statement_list -> statement statement_list | ε
        for t in ['int', 'float', 'string', 'identifier', 'if', 'while', 'input', 'print']:
            table['statement_list'][t] = 0
        for t in ['$', '}']:
            table['statement_list'][t] = 1
        
        # statement -> declaration | assignment | if_statement | while_statement | input_statement | print_statement
        for t in ['int', 'float', 'string']:
            table['statement'][t] = 0  # declaration
        table['statement']['identifier'] = 1  # assignment
        table['statement']['if'] = 2  # if_statement
        table['statement']['while'] = 3  # while_statement
        table['statement']['input'] = 4  # input_statement
        table['statement']['print'] = 5  # print_statement
        
        # declaration -> type identifier ;
        for t in ['int', 'float', 'string']:
            table['declaration'][t] = 0
        
        # type -> int | float | string
        table['type']['int'] = 0
        table['type']['float'] = 1
        table['type']['string'] = 2
        
        # assignment -> identifier = expression ;
        table['assignment']['identifier'] = 0
        
        # if_statement -> if ( condition ) { statement_list } else_part
        table['if_statement']['if'] = 0
        
        # else_part -> else { statement_list } | ε
        table['else_part']['else'] = 0
        for t in ['int', 'float', 'string', 'identifier', 'if', 'while', 'input', 'print', '$', '}']:
            if table['else_part'][t] is None:  # avoid overwriting
                table['else_part'][t] = 1
        
        # while_statement -> while ( condition ) { statement_list }
        table['while_statement']['while'] = 0
        
        # input_statement -> input ( identifier ) ;
        table['input_statement']['input'] = 0
        
        # print_statement -> print ( expression ) ;
        table['print_statement']['print'] = 0
        
        # condition -> expression comparison_op expression
        for t in ['identifier', 'integer', 'real', 'str_literal', '(']:
            table['condition'][t] = 0
        
        # comparison_op -> == | != | < | > | <= | >=
        table['comparison_op']['=='] = 0
        table['comparison_op']['!='] = 1
        table['comparison_op']['<'] = 2
        table['comparison_op']['>'] = 3
        table['comparison_op']['<='] = 4
        table['comparison_op']['>='] = 5
        
        # expression -> term expression_prime
        for t in ['identifier', 'integer', 'real', 'str_literal', '(']:
            table['expression'][t] = 0
        
        # expression_prime -> + term expression_prime | - term expression_prime | ε
        table['expression_prime']['+'] = 0
        table['expression_prime']['-'] = 1
        for t in [')', ';', '==', '!=', '<', '>', '<=', '>=']:
            table['expression_prime'][t] = 2
        
        # term -> factor term_prime
        for t in ['identifier', 'integer', 'real', 'str_literal', '(']:
            table['term'][t] = 0
        
        # term_prime -> * factor term_prime | / factor term_prime | % factor term_prime | ε
        table['term_prime']['*'] = 0
        table['term_prime']['/'] = 1
        table['term_prime']['%'] = 2
        for t in ['+', '-', ')', ';', '==', '!=', '<', '>', '<=', '>=']:
            table['term_prime'][t] = 3
        
        # factor -> identifier | integer | real | str_literal | ( expression )
        table['factor']['identifier'] = 0
        table['factor']['integer'] = 1
        table['factor']['real'] = 2
        table['factor']['str_literal'] = 3
        table['factor']['('] = 4
        
        return table

# Lexical Analyzer (Tokenizer)
class Tokenizer:
    def __init__(self):
        # Define token patterns
        self.token_patterns = [
            # Primero procesamos los comentarios para que tengan prioridad
            ('comment', r'//.*'),  # Comentarios con //
            ('comment', r'/\*[\s\S]*?\*/'),  # Comentarios estilo /* ... */
            ('comment', r'/[^/*].*'),  # Comentarios con un solo /
            
            # Después procesamos el resto de tokens
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
            (':', r':'),  # Agregado para manejar el caracter ':'
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
                    if token_type not in ['whitespace', 'comment']:  # Skip whitespace and comments
                        tokens.append((token_type, token_text, line, column))
                    
                    # Update line and column numbers
                    newlines = token_text.count('\n')
                    if newlines > 0:
                        line += newlines
                        column = len(token_text) - token_text.rfind('\n')
                    else:
                        column += len(token_text)
                    
                    pos += len(token_text)
                    break
            
            if not match:
                # Check if we've reached the end of the input
                if pos >= len(input_text):
                    break
                
                # No match found, report the error and skip the character
                error_char = input_text[pos]
                print(f"Error de tokenización en línea {line}, columna {column}: Carácter no reconocido '{error_char}'")
                
                # Update position and column
                if error_char == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                
                pos += 1
        
        tokens.append(('$', '$', line, column))  # End of input marker
        return tokens

# LL(1) Parser
class Parser:
    def __init__(self):
        self.grammar = Grammar()
        self.tokenizer = Tokenizer()
        self.tokens = []
        self.index = 0
        self.error_message = ""
        self.parse_tree = []
    
    def parse(self, input_text):
        # Tokenize the input
        self.tokens = self.tokenizer.tokenize(input_text)
        self.index = 0
        self.error_message = ""
        self.parse_tree = []
        
        # Initialize the stack with the start symbol and $
        stack = ['$', 'program']
        
        # Main parsing loop
        while stack[-1] != '$':
            top = stack[-1]
            current_token = self.tokens[self.index]
            current_token_type = current_token[0]
            
            # Debug information
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
            else:  # top is a non-terminal
                if current_token_type in self.grammar.parsing_table[top] and self.grammar.parsing_table[top][current_token_type] is not None:
                    production_idx = self.grammar.parsing_table[top][current_token_type]
                    production = self.grammar.productions[top][production_idx]
                    
                    self.parse_tree.append(f"Aplicar: {top} -> {' '.join(production)}")
                    
                    stack.pop()
                    
                    # Push the production in reverse order
                    for symbol in reversed(production):
                        if symbol != 'ε':
                            stack.append(symbol)
                else:
                    line, column = current_token[2], current_token[3]
                    self.error_message = f"Error de sintaxis en línea {line}, columna {column}: No hay producción para [{top}, {current_token_type}]"
                    self.parse_tree.append(f"Error: {self.error_message}")
                    return False, self.parse_tree
        
        # Check if we've consumed all input
        if self.index < len(self.tokens) - 1:  # -1 to account for the '$' token
            remaining_tokens = [t[1] for t in self.tokens[self.index:]]
            self.error_message = f"Error de sintaxis: Entrada no consumida por completo. Restante: {remaining_tokens}"
            self.parse_tree.append(f"Error: {self.error_message}")
            return False, self.parse_tree
        
        self.parse_tree.append("¡Análisis sintáctico exitoso!")
        return True, self.parse_tree

# Tkinter GUI
class ParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico LL(1)")
        self.root.geometry("1200x800")
        
        self.parser = Parser()
        
        self.create_widgets()
        self.load_example(0)  # Load the first example by default
    
    def create_widgets(self):
        # Create main frames
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input frame on the left
        input_frame = ttk.LabelFrame(left_frame, text="Código de Entrada")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=50, height=30, font=("Courier New", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Button frame below input
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        parse_button = ttk.Button(button_frame, text="Analizar", command=self.parse)
        parse_button.pack(side=tk.RIGHT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear)
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Examples frame below buttons
        examples_frame = ttk.LabelFrame(left_frame, text="Casos de Prueba")
        examples_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for i in range(5):
            example_button = ttk.Button(examples_frame, text=f"Caso {i+1}", command=lambda i=i: self.load_example(i))
            example_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Output frame on the right
        output_frame = ttk.LabelFrame(right_frame, text="Resultado del Análisis")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=50, height=40, font=("Courier New", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Grammar frame at the bottom
        grammar_frame = ttk.LabelFrame(right_frame, text="Referencia de Gramática")
        grammar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        grammar_text = "Gramática LL(1):\n"
        grammar_text += "program → statement_list\n"
        grammar_text += "statement_list → statement statement_list | ε\n"
        grammar_text += "statement → declaration | assignment | if_statement | while_statement | input_statement | print_statement\n"
        grammar_text += "declaration → type identifier ;\n"
        grammar_text += "type → int | float | string\n"
        grammar_text += "assignment → identifier = expression ;\n"
        grammar_text += "if_statement → if ( condition ) { statement_list } else_part\n"
        grammar_text += "else_part → else { statement_list } | ε\n"
        grammar_text += "while_statement → while ( condition ) { statement_list }\n"
        grammar_text += "input_statement → input ( identifier ) ;\n"
        grammar_text += "print_statement → print ( expression ) ;\n"
        grammar_text += "condition → expression comparison_op expression\n"
        grammar_text += "comparison_op → == | != | < | > | <= | >=\n"
        grammar_text += "expression → term expression_prime\n"
        grammar_text += "expression_prime → + term expression_prime | - term expression_prime | ε\n"
        grammar_text += "term → factor term_prime\n"
        grammar_text += "term_prime → * factor term_prime | / factor term_prime | % factor term_prime | ε\n"
        grammar_text += "factor → identifier | integer | real | str_literal | ( expression )"
        
        grammar_label = ttk.Label(grammar_frame, text=grammar_text, justify=tk.LEFT, font=("Courier New", 9))
        grammar_label.pack(padx=5, pady=5, anchor=tk.W)
    
    def parse(self):
        input_code = self.input_text.get("1.0", tk.END)
        success, parse_tree = self.parser.parse(input_code)
        
        self.output_text.delete("1.0", tk.END)
        
        for line in parse_tree:
            if line.startswith("Error:"):
                self.output_text.insert(tk.END, line + "\n")
                self.output_text.tag_add("error", f"{int(self.output_text.index('end-1c').split('.')[0]) - 1}.0", tk.END)
                self.output_text.tag_configure("error", foreground="red")
            elif line.startswith("¡Análisis sintáctico exitoso!"):
                self.output_text.insert(tk.END, line + "\n")
                self.output_text.tag_add("success", f"{int(self.output_text.index('end-1c').split('.')[0]) - 1}.0", tk.END)
                self.output_text.tag_configure("success", foreground="green")
            elif line.startswith("Coincidencia:"):
                self.output_text.insert(tk.END, line + "\n")
                self.output_text.tag_add("match", f"{int(self.output_text.index('end-1c').split('.')[0]) - 1}.0", tk.END)
                self.output_text.tag_configure("match", foreground="blue")
            elif line.startswith("Aplicar:"):
                self.output_text.insert(tk.END, line + "\n")
                self.output_text.tag_add("apply", f"{int(self.output_text.index('end-1c').split('.')[0]) - 1}.0", tk.END)
                self.output_text.tag_configure("apply", foreground="purple")
            else:
                self.output_text.insert(tk.END, line + "\n")
        
        # Show final result message
        if success:
            self.output_text.insert(tk.END, "\nÉxito: El código de entrada es sintácticamente correcto.\n")
            self.output_text.tag_add("final_success", f"{int(self.output_text.index('end-1c').split('.')[0]) - 1}.0", tk.END)
            self.output_text.tag_configure("final_success", foreground="green", font=("Arial", 12, "bold"))
        else:
            self.output_text.insert(tk.END, f"\nError: {self.parser.error_message}\n")
            self.output_text.tag_add("final_error", f"{int(self.output_text.index('end-1c').split('.')[0]) - 1}.0", tk.END)
            self.output_text.tag_configure("final_error", foreground="red", font=("Arial", 12, "bold"))
    
    def clear(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
    
    def load_example(self, example_num):
        self.clear()
        
        # Define example code snippets
        examples = [
            # Example 1: Variable declarations and assignment
            """/ Caso de prueba 1: Declaraciones de variables y asignaciones
int x;
float y;
string message;
x = 10;
y = 3.14;
message = "Hello, world!";
""",
            # Example 2: If-else statement
            """/ Caso de prueba 2: Sentencia if-else
int number;
number = 42;
if (number > 10) {
    print(number);
} else {
    print(0);
}
""",
            # Example 3: While loop
            """/ Caso de prueba 3: Ciclo while
int counter;
counter = 1;
while (counter <= 5) {
    print(counter);
    counter = counter + 1;
}
""",
            # Example 4: Input and arithmetic operations
            """/ Caso de prueba 4: Operaciones de entrada y aritméticas
int a;
int b;
input(a);
input(b);
int sum;
sum = a + b;
int product;
product = a * b;
print(sum);
print(product);
""",
            # Example 5: Syntax error example
            """/ Caso de prueba 5: Este contiene errores de sintaxis
int x;
x = 10;
if x > 5) { / Falta paréntesis de apertura
    print(x)  / Falta punto y coma
}
"""
        ]
        
        if 0 <= example_num < len(examples):
            self.input_text.insert(tk.END, examples[example_num])

# Main application
def main():
    root = tk.Tk()
    app = ParserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
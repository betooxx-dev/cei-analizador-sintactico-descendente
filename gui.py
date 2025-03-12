import tkinter as tk
from tkinter import ttk, scrolledtext
from parser import Parser
from test_cases import TestCases

class ParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Sintáctico LL(1)")
        self.root.geometry("1200x800")
        
        self.parser = Parser()
        
        self.create_widgets()
        self.load_example(0)  
    
    def create_widgets(self):
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        input_frame = ttk.LabelFrame(left_frame, text="Código de Entrada")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=50, height=30, font=("Courier New", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        parse_button = ttk.Button(button_frame, text="Analizar", command=self.parse)
        parse_button.pack(side=tk.RIGHT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Limpiar", command=self.clear)
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        examples_frame = ttk.LabelFrame(left_frame, text="Casos de Prueba")
        examples_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for i in range(5):
            example_button = ttk.Button(examples_frame, text=f"Caso {i+1}", command=lambda i=i: self.load_example(i))
            example_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        output_frame = ttk.LabelFrame(right_frame, text="Resultado del Análisis")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=50, height=40, font=("Courier New", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
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
        examples = TestCases.get_examples()
        
        if 0 <= example_num < len(examples):
            self.input_text.insert(tk.END, examples[example_num])
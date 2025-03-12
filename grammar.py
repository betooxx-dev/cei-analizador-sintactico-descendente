class Grammar:
    def __init__(self):
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
        
        self.parsing_table = self._create_parsing_table()
    
    def _create_parsing_table(self):
        table = {}
        for nt in self.non_terminals:
            table[nt] = {}
            for t in self.terminals + ['$']:
                table[nt][t] = None
        
        
        for t in ['int', 'float', 'string', 'identifier', 'if', 'while', 'input', 'print', '$']:
            table['program'][t] = 0
        
        for t in ['int', 'float', 'string', 'identifier', 'if', 'while', 'input', 'print']:
            table['statement_list'][t] = 0
        for t in ['$', '}']:
            table['statement_list'][t] = 1
        
        for t in ['int', 'float', 'string']:
            table['statement'][t] = 0  
        table['statement']['identifier'] = 1  
        table['statement']['if'] = 2  
        table['statement']['while'] = 3 
        table['statement']['input'] = 4 
        table['statement']['print'] = 5 

        for t in ['int', 'float', 'string']:
            table['declaration'][t] = 0

        table['type']['int'] = 0
        table['type']['float'] = 1
        table['type']['string'] = 2

        table['assignment']['identifier'] = 0

        table['if_statement']['if'] = 0

        table['else_part']['else'] = 0
        for t in ['int', 'float', 'string', 'identifier', 'if', 'while', 'input', 'print', '$', '}']:
            if table['else_part'][t] is None: 
                table['else_part'][t] = 1

        table['while_statement']['while'] = 0

        table['input_statement']['input'] = 0

        table['print_statement']['print'] = 0

        for t in ['identifier', 'integer', 'real', 'str_literal', '(']:
            table['condition'][t] = 0

        table['comparison_op']['=='] = 0
        table['comparison_op']['!='] = 1
        table['comparison_op']['<'] = 2
        table['comparison_op']['>'] = 3
        table['comparison_op']['<='] = 4
        table['comparison_op']['>='] = 5

        for t in ['identifier', 'integer', 'real', 'str_literal', '(']:
            table['expression'][t] = 0

        table['expression_prime']['+'] = 0
        table['expression_prime']['-'] = 1
        for t in [')', ';', '==', '!=', '<', '>', '<=', '>=']:
            table['expression_prime'][t] = 2

        for t in ['identifier', 'integer', 'real', 'str_literal', '(']:
            table['term'][t] = 0
        
        table['term_prime']['*'] = 0
        table['term_prime']['/'] = 1
        table['term_prime']['%'] = 2
        for t in ['+', '-', ')', ';', '==', '!=', '<', '>', '<=', '>=']:
            table['term_prime'][t] = 3
        
        table['factor']['identifier'] = 0
        table['factor']['integer'] = 1
        table['factor']['real'] = 2
        table['factor']['str_literal'] = 3
        table['factor']['('] = 4
        
        return table
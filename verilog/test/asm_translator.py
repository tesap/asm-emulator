#!/usr/local/bin/python3

import re, sys
# Very simple symbol table for the assembler.

SYMBOLS_ADDR = 16

class SymbolTable(object):
    def __init__(self):
        # Predefined symbols equate to memory locations
        self._symbols \
            = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
               'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
               'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
               'SCREEN':0x4000, 'KBD':0x6000}
                    
    def add_entry(self, symbol, address):
        self._symbols[symbol] = address
        
    def contains(self, symbol):
        return symbol in self._symbols
        
    def get_address(self, symbol):
        return self._symbols[symbol]#!/usr/local/bin/python3


NUM     = 1     # number e.g. '123'
ID      = 2     # symbol e.g. 'LOOP'
OP      = 3     # = ; ( ) @ + - & | !
ERROR   = 4     # error in file

# Lexer is very simple.  Almost no error checking! - Assumes input will be program-generated.
# Detects numbers, Ids, and operators.
# Reads the whole .asm program into memory and uses regular expressions to match lexical tokens.

class Lex(object):            
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self._lines = file.read()
        self._tokens = self._tokenize(self._lines.split('\n'))
        self.cur_command = []        # list of tokens for current command
        self.cur_token = (ERROR,0)   # current token of current command   
    
    def __str__(self):
        pass
        
    def has_more_commands(self):
        return self._tokens != []
        
    def next_command(self):
        self.cur_command = self._tokens.pop(0)
        self.next_token()
        return self.cur_command
        
    def has_next_token(self):
        return self.cur_command != []
        
    def next_token(self):
        if self.has_next_token():
            self.cur_token = self.cur_command.pop(0)
        else:
            self.cur_token = (ERROR, 0)
        return self.cur_token
        
    def peek_token(self):
        if self.has_next_token():
            return self.cur_command[0]
        else:
            return (ERROR, 0)
        
    def _tokenize(self, lines):
        return [t for t in [self._tokenize_line(l) for l in lines] if t!=[]]
    
    def _tokenize_line(self, line):
        return [self._token(word) for word in self._split(self._remove_comment(line))]
	
    _comment = re.compile('//.*$')
    def _remove_comment(self, line):
        return self._comment.sub('', line)

    _num_re = r'\d+'
    _id_start = r'\w_.$:'
    _id_re = '['+_id_start+']['+_id_start+r'\d]*'
    _op_re = r'[=;()@+\-&|!]'
    _word = re.compile(_num_re+'|'+_id_re+'|'+_op_re)
    def _split(self, line):
        return self._word.findall(line)
		
    def _token(self, word):
        if   self._is_num(word):     return (NUM, word)
        elif self._is_id(word):      return (ID, word)
        elif self._is_op(word):      return (OP, word)
        else:                        return (ERROR, word)
			
    def _is_op(self, word):
        return self._is_match(self._op_re, word)
        
    def _is_num(self, word):
        return self._is_match(self._num_re, word)
        
    def _is_id(self, word):
        return self._is_match(self._id_re, word)
        
    def _is_match(self, re_str, word):
        return re.match(re_str, word) != None#!/usr/local/bin/python3


# Parser assumes correctly-formed input - no error checking!  Expects program-generated input.
# Would do a recursive-descent parser for fun, but it's just overkill for this.
# Parser just looks ahead one or two tokens to determine what's there.

class Parser(object):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    
    def __init__(self, file):
        self.lex = Lex(file)
        self._init_cmd_info()
    
    def _init_cmd_info(self):
        self._cmd_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''
    
    def __str__(self):
        pass
        
    def has_more_commands(self):
        return self.lex.has_more_commands()
    
    # Get the next entire command - each command resides on its own line.
    def advance(self):
        self._init_cmd_info()

        self.lex.next_command()
        tok, val = self.lex.cur_token

        if tok == OP and val == '@':
            self._a_command()
        elif tok == OP and val == '(':
            self._l_command()
        else:
            self._c_command(tok, val)
    
    # The following functions contain the extracted parts of the command.
    
    def command_type(self):
        return self._cmd_type 
        
    def symbol(self):
        return self._symbol
    
    def dest(self):
        return self._dest
    
    def comp(self):
        return self._comp
        
    def jmp(self):
        return self._jmp
        
    # @symbol or @number
    def _a_command(self):
        self._cmd_type = Parser.A_COMMAND
        tok_type, self._symbol = self.lex.next_token()
        
    # (symbol)
    def _l_command(self):
        self._cmd_type = Parser.L_COMMAND
        tok_type, self._symbol = self.lex.next_token()

    # dest=comp;jump
    # dest=comp         omitting jump
    # comp;jump         omitting dest
    # comp              omitting dest and jump
    def _c_command(self, tok1, val1):
        self._cmd_type = Parser.C_COMMAND
        comp_tok, comp_val = self._get_dest(tok1, val1)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    # Get the 'dest' part if any.  Return the first token of the 'comp' part.
    def _get_dest(self, tok1, val1):
        tok2, val2 = self.lex.peek_token()
        if tok2 == OP and val2 == '=':
            self.lex.next_token()
            self._dest = val1
            comp_tok, comp_val = self.lex.next_token()
        else:
            comp_tok, comp_val = tok1, val1
        return (comp_tok, comp_val)
    
    # Get the 'comp' part - must be present.
    def _get_comp(self, tok, val):
        if tok == OP and (val == '-' or val == '!'):
            tok2, val2 = self.lex.next_token()
            self._comp = val+val2
        elif tok == NUM or tok == ID:
            self._comp = val
            tok2, val2 = self.lex.peek_token()
            if tok2 == OP and val2 != ';':
                self.lex.next_token()
                tok3, val3 = self.lex.next_token()
                self._comp += val2+val3
        
    # Get the 'jump' part if any
    def _get_jump(self):
        tok, val = self.lex.next_token()
        if tok == OP and val == ';':
            jump_tok, jump_val = self.lex.next_token()
            self._jmp = jump_val#!/usr/local/bin/python3

# Generates the code bit-strings from the parsed instruction parts.
# The code generator just outputs a text files with one 16-bit instruction per line
# as textual strings of 1's and 0's.

class Code(object):
    def __init__(self):
        pass
    
    def gen_a(self, addr):
        return '0' + self._bits(addr).zfill(15);
        
    def gen_c(self, dest, comp, jump):
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)
    
    _dest_codes = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
    def dest(self, d):
        return self._bits(self._dest_codes.index(d)).zfill(3)
    
    _comp_codes = { '0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
                    'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
                    '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110', 
                    'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111', 
                    'D&A':'0000000','D|A':'0010101',
                    '':'xxxxxxx',   '':'xxxxxxx',   '':'xxxxxxx',   '':'xxxxxxx', 
                    'M':'1110000',  '':'xxxxxxx',   '!M':'1110001', '':'xxxxxxx', 
                    '-M':'1110011', '':'xxxxxxx',   'M+1':'1110111','':'xxxxxxx', 
                    'M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111', 
                    'D&M':'1000000', 'D|M':'1010101' }
    def comp(self, c):
        return self._comp_codes[c]
    
    _jump_codes = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
    def jump(self, j):
        return self._bits(self._jump_codes.index(j)).zfill(3)
        
    def _bits(self, n):
        return bin(int(n))[2:]#!/usr/local/bin/python3
        

# Usage: Assembler.py file.asm
# Reads file.asm and outputs file.hack - the assembled machine code as a text file.

class Assembler(object):
    def __init__(self):
        self.symbols = SymbolTable()
    
    # First pass: determine memory locations of label definitions: (LABEL)
    def pass0(self, file):
        parser = Parser(file)
        cur_address = 0
        while parser.has_more_commands():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.A_COMMAND or cmd == parser.C_COMMAND:
                cur_address += 1
            elif cmd == parser.L_COMMAND:
                self.symbols.add_entry( parser.symbol(), cur_address )
    
    # Second pass: generate code and write result to output file.
    def pass1(self, infile):
        result = ""

        parser = Parser(infile)
        code = Code()
        while parser.has_more_commands():
            parser.advance()
            cmd = parser.command_type()
            if cmd == parser.A_COMMAND:
                result += code.gen_a(self._get_address(parser.symbol())) + '\n'
            elif cmd == parser.C_COMMAND:
                result += code.gen_c(parser.dest(), parser.comp(), parser.jmp()) + '\n'
            elif cmd == parser.L_COMMAND:
                pass

        print(result)
    
    # Lookup an address - may be symbolic, or already numeric
    def _get_address(self, symbol):
        global SYMBOLS_ADDR

        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols.contains(symbol):
                self.symbols.add_entry(symbol, SYMBOLS_ADDR)
                SYMBOLS_ADDR += 1
            return self.symbols.get_address(symbol)
    
    # Drive the assembly process
    def assemble(self, file):
        self.pass0( file )
        self.pass1( file )
        
    def _outfile(self, infile):
        if infile.endswith( '.asm' ):
            return infile.replace( '.asm', '.hack' )
        else:
            return infile + '.hack'    

def main():
    if len(sys.argv) != 2:
        print( "Usage: Assembler file.asm" )
    else:
        infile = sys.argv[1]
        
    asm = Assembler()
    asm.assemble( infile )
    
main()

#! /usr/bin/env python

from tokenizer import Tokenizer

def token_generator():
    with open('./input.c') as input_file:
        tokenizer = Tokenizer(input_file).token_generator()
        for token in tokenizer:
            yield token

token_stream = token_generator()
token_buffer = []
def next_token():
    """
    fetch the next token
    returns None if no more tokens exist
    """
    global token_buffer
    if token_buffer:
        tok = token_buffer[0]
        token_buffer = token_buffer[1:]
        return tok
    try:
        return next(token_stream)
    except StopIteration:
        return None

token = next_token()

def match(token_type):
    global token
    if token.type == token_type:
        value = token.value
        token = next_token()
        print("------" + str(token))
        return value # return value of a token
    else:
        raise Exception('PARSE ERROR')

def peek(offset):
    """
    token == peek(0)
    """
    if offset == 0:
        return token

    # tok = None
    for _ in range(offset):
        try:
            tok = next(token_stream)
        except StopIteration:
            return None
        token_buffer.append(tok)
    return tok

def skip_new_lines():
    while token and token.type == 'NEW_LINE':
        match('NEW_LINE')

class Block():
    def __init__(self):
        self.units = []
        self.parse()

    def parse(self):
        # ENTRY
        while token and (token.type == 'ID' or token.type == 'BUILTIN_TYPE' \
            or token.type == 'WHILE' or token.type == 'IF'):
            unit = BlockUnit()
            self.units.append(unit)
            skip_new_lines()

    def __str__(self):
        return '\n'.join(map(str, self.units))

class BlockUnit():
    def __init__(self):
        self.type = None
        self.core = None
        self.parse()

    def parse(self):
        if token.type == 'ID' or token.type == 'BUILTIN_TYPE':
            self.type = 'statement'
            self.core = Statement()
        elif token.type == 'WHILE':
            self.type = 'while'
            self.core = While()
        elif token.type == 'IF':
            self.type = 'if'
            self.core = If()

    def __str__(self):
        return str(self.core)

class While():
    def __init__(self):
        self.expression = None
        self.block = None
        self.parse()

    def parse(self):
        match('WHILE')
        match('OP')
        self.expression = Expression()
        match('CP')
        match('OB')
        self.block = Block()
        match('CB')

    def __str__(self):
        return '%s (%s) {\n%s\n}' % ('[while]', self.expression, self.block)

class If():
    def __init__(self):
        self.expression = None
        self.block = None
        self.parse()

    def parse(self):
        match('IF')
        match('OP')
        self.expression = Expression()
        match('CP')
        match('OB')
        self.block = Block()
        match('CB')

    def __str__(self):
        return '%s (%s) {\n%s\n}' % ('[if]', self.expression, self.block)

class Definition():
    def __init__(self):
        self.type = None
        self.id = None
        self.assigner = None
        self.parse()

    def parse(self):
        self.type = match('BUILTIN_TYPE')
        self.id = match('ID')
        match('ASSIGN')
        self.assigner = Expression()

    def __str__(self):
        return '[%s] %s %s = %s' % ('definition', self.type, self.id, self.assigner)

class Statement():
    def __init__(self):
        self.type = None
        self.core = None
        self.parse()

    def parse(self):
        if token.type == 'BUILTIN_TYPE':
            self.type = 'definition'
            self.core = Definition()
        else:
            self.type = 'expression'
            self.core = Expression()

        match('SEMICOLON')

    def __str__(self):
        return str(self.core) + ';'

class Expression():
    def __init__(self):
        self.type = None
        self.id = None
        self.core = None
        self.parse()

    def parse(self):
        if token.type == 'ID' and peek(1).type == 'ASSIGN':
            self.type = 'assignment'
            self.id = match('ID')
            match('ASSIGN')
            self.core = Expression()
        else:
            self.type = 'equality_expression'
            self.core = EqualityExpr()

    def __str__(self):
        if self.type == 'assignment':
            return '[assignment] %s = %s' % (self.id, self.core)
        else:
            return '%s' % self.core

class EqualityExpr():
    def __init__(self):
        self.operands = []
        self.ops = []
        self.parse()

    def parse(self):
        self.operands.append(RelationalExpr())
        while token.type in ['EQ', 'NE']:
            self.ops.append(match(token.type))
            self.operands.append(RelationalExpr())

    def __str__(self):
        return ''.join(zip_operands(self.operands, self.ops))

class RelationalExpr():
    def __init__(self):
        self.operands = []
        self.ops = []
        self.parse()

    def parse(self):
        self.operands.append(AdditiveExpr())
        while token.type in ['LT', 'LE', 'GT', 'GE']:
            self.ops.append(match(token.type))
            self.operands.append(AdditiveExpr())

    def __str__(self):
        return ''.join(zip_operands(self.operands, self.ops))

class AdditiveExpr():
    def __init__(self):
        self.operands = []
        self.ops = []
        self.parse()

    def parse(self):
        self.operands.append(MultiplicativeExpr())
        while token.type in ['PLUS', 'MINUS']:
            self.ops.append(match(token.type))
            self.operands.append(MultiplicativeExpr())

    def __str__(self):
        return ' '.join(zip_operands(self.operands, self.ops))

class MultiplicativeExpr():
    def __init__(self):
        self.operands = []
        self.ops = []
        self.parse()

    def parse(self):
        self.operands.append(UnaryExpr())
        while token.type in ['MULTIPLY', 'DIVIDE', 'MOD']:
            self.ops.append(match(token.type))
            self.operands.append(UnaryExpr())

    def __str__(self):
        return ' '.join(zip_operands(self.operands, self.ops))

class UnaryExpr():
    def __init__(self):
        self.ops = []
        self.core = None
        self.parse()

    def parse(self):
        while token.type in ['PLUS', 'MINUS', 'NOT']:
            self.ops.append(match(token.type))

        self.core = PrimaryExpr()

    def __str__(self):
        return '%s%s' % (''.join(self.ops), self.core)

class PrimaryExpr():
    def __init__(self):
        self.core = None
        self.type = None
        self.parse()

    def parse(self):
        if token.type == 'STRING':
            self.type = 'string'
            self.core = match('STRING')
        elif token.type == 'INTEGER':
            self.type = 'integer'
            self.core = match('INTEGER')
        elif token.type == 'ID':
            self.type = 'reference'
            self.core = match('ID')
        elif token.type == 'OP':
            self.type = 'expression'
            match('OP')
            self.core = Expression()
            match('CP')

    def __str__(self):
        return '[%s] %s' % (self.type, str(self.core))

def zip_operands(operands, ops):
    rest_pairs = [[ops[i], str(operands[i+1])] for i in range(len(ops))]
    seq = [str(operands[0])]
    for p in rest_pairs:
        seq += p
    return seq

tree = Block()
print(tree)

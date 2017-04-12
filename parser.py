#! /usr/bin/env python

from tokenizer import Tokenizer

def token_generator():
    with open('./input.c') as input_file:
        tokenizer = Tokenizer(input_file).token_generator()
        for token in tokenizer:
            yield token
token_stream = token_generator()
def next_token():
    """
    fetch the next token
    returns None if no more tokens exist
    """
    try:
        return next(token_stream)
    except StopIteration:
        return None

token = next_token()

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
        self.core = None
        self.parse()

    def parse(self):
        if token.type == 'STRING':
            self.core = match('STRING')
        elif token.type == 'ID':
            self.core = Assignference()

    def __str__(self):
        return str(self.core)

class Assignference():
    def __init__(self):
        self.id = None
        self.value = None
        self.type = None
        self.parse()

    def parse(self):
        self.id = match('ID')
        self.type = 'reference'
        if token.type == 'ASSIGN':
            match('ASSIGN')
            self.type = 'assignment'
            self.value = Expression()

    def __str__(self):
        if self.type == 'assignment':
            return '[%s] %s = %s' % (self.type, self.id, self.value)
        elif self.type == 'reference':
            return '[%s] %s' % (self.type, self.id)

def match(token_type):
    global token
    if token.type == token_type:
        value = token.value
        token = next_token()
        print("------" + str(token))
        return value # return value of a token
    else:
        raise Exception('PARSE ERROR')

def skip_new_lines():
    while token and token.type == 'NEW_LINE':
        match('NEW_LINE')

tree = Block()
print(tree)



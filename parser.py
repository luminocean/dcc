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
        self.statements = []
        self.parse()

    def parse(self):
        while token:
            stmt = Statement()
            self.statements.append(stmt)
            match('NEW_LINE')

    def __str__(self):
        return '\n'.join(map(str, self.statements))

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
        self.id = match('ID')
        self.assigner = None
        if token.type == 'ASSIGN':
            match('ASSIGN')
            self.assigner = Expression()

    def __str__(self):
        if self.assigner:
            return "[%s] %s = %s" % ('assginment', self.id, self.assigner)
        else:
            return "[%s] %s" % ('reference', self.id)

def match(token_type):
    global token
    if token.type == token_type:
        value = token.value
        token = next_token()
        return value # return value of a token
    else:
        raise Exception('PARSE ERROR')

tree = Block()
print(tree)



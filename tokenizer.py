import re
from collections import OrderedDict

TOKEN_REGEXES = OrderedDict([
    ('SEMICOLON', re.compile(r'(;)')),
    ('BUILTIN_TYPE', re.compile(r'(int|float)')),
    ('INTEGER', re.compile(r'((?:0|[1-9])\d*)')),
    ('WHILE', re.compile(r'(while)')),
    ('IF', re.compile(r'(if)')),
    ('STRING', re.compile(r'"(.*)(?<!\\)"')),
    ('ID', re.compile(r'([a-z][a-z0-9_]*)(?!a-z0-9)')),
    ('ASSIGN', re.compile(r'(=)[^=]')),
    ('NEW_LINE', re.compile(r'(\n)')),
    ('OP', re.compile(r'(\()')),
    ('CP', re.compile(r'(\))')),
    ('OB', re.compile(r'({)')),
    ('CB', re.compile(r'(})')),
    ('PLUS', re.compile(r'(\+)')),
    ('MINUS', re.compile(r'(-)')),
    ('NOT', re.compile(r'(!)')),
    ('MULTIPLY', re.compile(r'(\*)')),
    ('DIVIDE', re.compile(r'(\\)')),
    ('MOD', re.compile(r'(%)')),
    ('EQ', re.compile(r'(==)')),
    ('GT', re.compile(r'(>)')),
    ('GE', re.compile(r'(>=)')),
    ('LT', re.compile(r'(<)')),
    ('LE', re.compile(r'(<=)')),
    ('NE', re.compile(r'(!=)'))
])

class Token():
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        return '(%s, %s)' % (self.type, self.value)

class Tokenizer():
    def __init__(self, input_file):
        self.input_file = input_file

    def token_generator(self):
        buffer = ''
        batch = self.input_file.read(256)
        while batch:
            buffer += batch
            for token, buffer in self._analyze_token(buffer):
                if token:
                    yield token
            batch = self.input_file.read(256)

    def _analyze_token(self, buffer):
        has_match = True
        while has_match:
            has_match = False
            buffer = buffer.lstrip()
            for token_type, reg in TOKEN_REGEXES.items():
                m = reg.match(buffer)
                if m:
                    has_match = True
                    token = Token(token_type, m[1])
                    buffer = buffer[len(m[0]):]
                    yield (token, buffer)
                    break # start a new loop
            if not has_match: # no match in this batch, stop iteration
                break
        return (None, buffer)

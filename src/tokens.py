import math
import operator

NUMBERS = '0123456789.'
SPACE = ' '
HYPHEN = '-'
MINUS_SIGN = u"\u2212"
OPEN_PARENTHESES = '('
CLOSE_PARENTHESES = ')'
CONSTANTS = {'pi': math.pi, 'e': math.e, 'phi': 1.618033988749894}

FUNCTIONS = {'sqrt': (math.sqrt, 1),
             'cbrt': (lambda v: v ** (1. / 3), 1),
             'sin': (math.sin, 1),
             'cos': (math.cos, 1),
             'tan': (math.tan, 1),
             'radians': (math.radians, 1),
             'degrees': (math.degrees, 1)}

OPERATORS = {'+': (operator.add, 2, 'left', 2),
             '-': (operator.sub, 2, 'left', 2),
             '/': (operator.truediv, 3, 'left', 2),
             '*': (operator.mul, 3, 'left', 2),
             '^': (operator.pow, 4, 'right', 2),
             '!': (math.factorial, 5, 'left', 1),
             '-u': (lambda v: -v, 5, 'right', 1)}


class Token:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.symbol})"


class Value:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.value})"


class Operator(Token):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.function = OPERATORS[symbol][0]
        self.precedence = OPERATORS[symbol][1]
        self.associativity = OPERATORS[symbol][2]
        self.operands_count = OPERATORS[symbol][3]

    def __eq__(self, other):
        return super().__eq__(other) and self.operands_count == other.operands_count


class Function(Token):
    def __init__(self, function):
        super().__init__(function)
        self.function = FUNCTIONS[function][0]
        self.operands_count = FUNCTIONS[function][1]


class Variable(Token):
    def __init__(self, symbol):
        super().__init__(symbol)


class Constant(Token, Value):
    def __init__(self, symbol):
        Token.__init__(self, symbol)
        Value.__init__(self,CONSTANTS[symbol])


class OpenParentheses(Token):
    def __init__(self):
        super().__init__('(')


class CloseParentheses(Token):
    def __init__(self):
        super().__init__(')')

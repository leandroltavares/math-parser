from tokens import OPEN_PARENTHESES, CLOSE_PARENTHESES, OpenParentheses, CloseParentheses, NUMBERS, FUNCTIONS, \
    CONSTANTS, OPERATORS, Constant, Value, Variable, Operator, Function
from errors import UnmatchingOpenParentheses, UnmatchingCloseParentheses, UnexpectedCharacter
import re


class Tokenizer:
    def tokenize(self, expression):
        expression = self.expand_implicit_expression(expression)
        tokens = []
        variables = set()
        parentheses_level = 0
        current_char_sequence = []
        for position, char in enumerate(expression):
            self._evaluate_unexpected_char(position, char, expression)
            self._generate_new_token(tokens, current_char_sequence, variables, char)
            if char == OPEN_PARENTHESES:
                parentheses_level += 1
                tokens.append(OpenParentheses())
            elif char == CLOSE_PARENTHESES:
                parentheses_level -= 1
                tokens.append(CloseParentheses())
            elif char in NUMBERS or char.isalpha():
                current_char_sequence += char
            elif char in OPERATORS.keys():
                tokens.append(self._generate_operator(char, tokens))
            self._evaluate_matching_parentheses(parentheses_level, position, len(expression))
        self._generate_new_token(tokens, current_char_sequence, variables)
        return tokens, variables

    @staticmethod
    def expand_implicit_expression(expression):
        expression = expression.replace(')(', ')*(')
        expression = re.sub(r"(\d+)([a-zA-Z]+)", r"\1*\2", expression)
        expression = re.sub(r"([a-zA-Z]+)(\d+)", r"\1*\2", expression)
        expression = re.sub(r"(\d+)(\()", r"\1*\2", expression)
        expression = re.sub(r"(\))(\d+)", r"\1*\2", expression)
        return expression

    def _generate_new_token(self, tokens, current_char_sequence, variables, current_char=None):
        if self._should_generate_new_token(current_char_sequence, current_char):
            token = "".join(current_char_sequence)
            if token in CONSTANTS.keys():
                tokens.append(Constant(token))
            elif token in FUNCTIONS.keys():
                tokens.append(Function(token))
            elif token.isalpha():
                variables.add(token)
                tokens.append(Variable(token))
            else:
                tokens.append(Value(token))
            current_char_sequence.clear()

    @staticmethod
    def _should_generate_new_token(current_char_sequence, current_char):
        return current_char_sequence and (current_char is None
                                          or current_char in {OPEN_PARENTHESES, CLOSE_PARENTHESES}
                                          or current_char in OPERATORS.keys())

    @staticmethod
    def _evaluate_matching_parentheses(parentheses_level, position, length):
        if parentheses_level <= -1:
            raise UnmatchingCloseParentheses(position)
        if position == length - 1 and parentheses_level > 0:
            raise UnmatchingOpenParentheses()

    @staticmethod
    def _evaluate_unexpected_char(position, current_char, expression):
        previous_char = expression[position - 1]
        if (current_char == '.' and previous_char == '.') or (current_char == ')' and previous_char == '('):
            raise UnexpectedCharacter(position)

    @staticmethod
    def _generate_operator(op, tokens):
        if op == "-" and (not tokens or isinstance(tokens[-1], Operator)):
            op = '-u'
        return Operator(op)


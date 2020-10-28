import unittest
from errors import UnmatchingOpenParentheses, UnmatchingCloseParentheses, UnexpectedCharacter
from tokenizer import Tokenizer, Value, Operator, Constant, Variable, Function, OpenParentheses, CloseParentheses


class TokenizerTest(unittest.TestCase):

    def test_parse_unmatching_open_parentheses_raise_exception(self):
        t = Tokenizer()
        with self.assertRaises(UnmatchingOpenParentheses):
            t.tokenize('((1)')

    def test_parse_unmatching_close_parentheses_raise_exception(self):
        t = Tokenizer()
        with self.assertRaises(UnmatchingCloseParentheses):
            t.tokenize('(1))')

    def test_parser_multiple_dots_raise_exception(self):
        t = Tokenizer()
        with self.assertRaises(UnexpectedCharacter):
            t.tokenize('1..1')

    def test_parser_empty_parenthesis_raise_exception(self):
        t = Tokenizer()
        with self.assertRaises(UnexpectedCharacter):
            t.tokenize('()')

    def test_parse_multiple_digits_number(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('42')
        expected_tokens = [Value('42')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_longer_number(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('42.0')
        expected_tokens = [Value('42.0')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_decimal_number_without_zero_prefix(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('.1')
        expected_tokens = [Value('.1')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_negative_number(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('-42')
        expected_tokens = [Operator('-u'), Value('42')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_simple_addition_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('1+2')
        expected_tokens = [Value('1'), Operator('+'), Value('2')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_simple_addition_expression_with_negative_numbers(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('-1+(-2)')
        expected_tokens = [Operator('-u'), Value('1'), Operator('+'), OpenParentheses(), Operator('-'), Value('2'),
                           CloseParentheses()]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_negative_variable(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('-x')
        expected_tokens = [Operator('-u'), Variable('x')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual({'x'}, variables)

    def test_parse_subtraction_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('2-1')
        expected_tokens = [Value('2'), Operator('-'), Value('1')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_multiplication_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('2*3')
        expected_tokens = [Value('2'), Operator('*'), Value('3')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_division_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('4/2')
        expected_tokens = [Value('4'), Operator('/'), Value('2')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_composed_addition_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('(1+2)*3')
        expected_tokens = [OpenParentheses(), Value('1'), Operator('+'), Value('2'), CloseParentheses(), Operator('*'),
                           Value('3')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_composed_complex_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('((1+2)*3+pi)*x/2+sin(1)')
        expected_tokens = [OpenParentheses(), OpenParentheses(), Value('1'), Operator('+'), Value('2'),
                           CloseParentheses(), Operator('*'), Value('3'), Operator('+'), Constant('pi'),
                           CloseParentheses(), Operator('*'), Variable('x'), Operator('/'), Value('2'), Operator('+'),
                           Function('sin'), OpenParentheses(), Value('1'), CloseParentheses()]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual({'x'}, variables)

    def test_parse_implicit_parentheses_multiplication(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('(1+2)(3+4)')
        expected_tokens = [OpenParentheses(), Value('1'), Operator('+'), Value('2'), CloseParentheses(), Operator('*'),
                           OpenParentheses(), Value('3'), Operator('+'), Value('4'), CloseParentheses()]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_implicit_parentheses_multiplication2(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('2(1+2)')
        expected_tokens = [Value('2'), Operator('*'), OpenParentheses(), Value('1'), Operator('+'), Value('2'),
                           CloseParentheses()]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_implicit_parentheses_multiplication3(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('(1+2)2')
        expected_tokens = [OpenParentheses(), Value('1'), Operator('+'), Value('2'), CloseParentheses(), Operator('*'),
                           Value('2')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_implicit_constant_multiplication(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('10pi')
        expected_tokens = [Value('10'), Operator('*'), Constant('pi')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_implicit_constant_multiplication2(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('pi10')
        expected_tokens = [Constant('pi'), Operator('*'), Value('10')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual(0, len(variables))

    def test_parse_implicit_constant_multiplication_expression(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('2pi * r')
        expected_tokens = [Value('2'), Operator('*'), Constant('pi'), Operator('*'), Variable('r')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual({'r'}, variables)

    def test_parse_implicit_function_multiplication(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('10sin(x)')
        expected_tokens = [Value('10'), Operator('*'), Function('sin'), OpenParentheses(), Variable('x'),
                           CloseParentheses()]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual({'x'}, variables)

    def test_parse_implicit_function_multiplication2(self):
        t = Tokenizer()
        tokens, variables = t.tokenize('sin(x)10')
        expected_tokens = [Function('sin'), OpenParentheses(), Variable('x'), CloseParentheses(), Operator('*'),
                           Value('10')]
        self.assertEqual(expected_tokens, tokens)
        self.assertEqual({'x'}, variables)

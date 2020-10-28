import unittest
from expression import Expression


class ParserTest(unittest.TestCase):
    def test_parse_constant_expression(self):
        e = Expression()
        e.parse('1')
        self.assertEqual(1, e.evaluate())

    def test_parse_negative_constant_expression(self):
        e = Expression()
        e.parse('-1')
        self.assertEqual(-1, e.evaluate())

    def test_parse_addition_expression(self):
        e = Expression()
        e.parse('1+2')
        self.assertEqual(3, e.evaluate())

    def test_parse_subtraction_expression(self):
        e = Expression()
        e.parse('1-2')
        self.assertEqual(-1, e.evaluate())

    def test_parse_division_expression(self):
        e = Expression()
        e.parse('1/2')
        self.assertEqual(0.5, e.evaluate())

    def test_parse_multiplication_expression(self):
        e = Expression()
        e.parse('1*2')
        self.assertEqual(2, e.evaluate())

    def test_pi_constant_expression(self):
        e = Expression()
        e.parse('pi')
        self.assertAlmostEqual(3.1416, e.evaluate(), 4)

    def test_phi_constant_expression(self):
        e = Expression()
        e.parse('phi')
        self.assertAlmostEqual(1.6180, e.evaluate(), 4)

    def test_e_constant_expression(self):
        e = Expression()
        e.parse('e')
        self.assertAlmostEqual(2.718, e.evaluate(), 2)

    def test_parse_exponential_expression(self):
        e = Expression()
        e.parse('2^10')
        self.assertEqual(1024, e.evaluate())

    def test_parse_sin0_expression(self):
        e = Expression()
        e.parse('sin(0)')
        self.assertEqual(0, e.evaluate())

    def test_parse_sin90_expression2(self):
        e = Expression()
        e.parse('sin(pi/2)')
        self.assertEqual(1, e.evaluate())

    def test_parse_factorial_expression(self):
        e = Expression()
        e.parse('0!')
        self.assertEqual(1, e.evaluate())

    def test_parse_factorial_expression2(self):
        e = Expression()
        e.parse('1!')
        self.assertEqual(1, e.evaluate())

    def test_parse_factorial_expression3(self):
        e = Expression()
        e.parse('5!')
        self.assertEqual(120, e.evaluate())

    def test_parse_addition_expression_with_variable(self):
        e = Expression()
        e.parse('x+1')
        e.assign_value('x', 1)
        self.assertEqual(2, e.evaluate())

    def test_parse_expression_with_multiple_variables(self):
        e = Expression()
        e.parse('x+y')
        e.assign_value('x', 1)
        e.assign_value('y', 2)
        self.assertEqual(3, e.evaluate())

    def test_parse_expression_with_multiple_ocurrences_of_same_variable(self):
        e = Expression()
        e.parse('x*x')
        e.assign_value('x', 10)
        self.assertEqual(100, e.evaluate())

    def test_parse_with_parentheses(self):
        e = Expression()
        e.parse('((1)+(2))*3')
        self.assertEqual(9, e.evaluate())

    # def test_parse_long_expression(self):
    #     e = Expression()
    #     e.parse('3 + 4 * 2 / ( 1 − 5 ) ^ 2 ^ 3')
    #     self.assertEqual(3.0001220703125, e.evaluate())


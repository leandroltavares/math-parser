import unittest
import math
from expression import Expression
from errors import UnassignedVariable


class ParserTest(unittest.TestCase):
    def test_evaluate_constant_expression(self):
        e = Expression('1')
        self.assertEqual(1, e.evaluate())

    def test_evaluate_negative_constant_expression(self):
        e = Expression('-1')
        self.assertEqual(-1, e.evaluate())

    def test_evaluate_addition_expression(self):
        e = Expression('1+2')
        self.assertEqual(3, e.evaluate())

    def test_evaluate_subtraction_expression(self):
        e = Expression('1-2')
        self.assertEqual(-1, e.evaluate())

    def test_evaluate_division_expression(self):
        e = Expression('1/2')
        self.assertEqual(0.5, e.evaluate())

    def test_evaluate_multiplication_expression(self):
        e = Expression('1*2')
        self.assertEqual(2, e.evaluate())

    def test_pi_constant_expression(self):
        e = Expression('pi')
        self.assertAlmostEqual(3.1416, e.evaluate(), 4)

    def test_phi_constant_expression(self):
        e = Expression('phi')
        self.assertAlmostEqual(1.6180, e.evaluate(), 4)

    def test_e_constant_expression(self):
        e = Expression('e')
        self.assertAlmostEqual(2.718, e.evaluate(), 2)

    def test_evaluate_exponential_expression(self):
        e = Expression('2^10')
        self.assertEqual(1024, e.evaluate())

    def test_evaluate_sin0_expression(self):
        e = Expression('sin(0)')
        self.assertEqual(0, e.evaluate())

    def test_evaluate_sin90_expression_in_radians(self):
        e = Expression('sin(pi/2)')
        self.assertEqual(1, e.evaluate())

    def test_evaluate_sin90_expression_in_degrees(self):
        e = Expression('sin(radians(90))')
        self.assertEqual(1, e.evaluate())

    def test_evaluate_cos0_expression(self):
        e = Expression('cos(0)')
        self.assertEqual(1, e.evaluate())

    def test_evaluate_cos90_expression_in_radians(self):
        e = Expression('cos(pi/2)')
        self.assertAlmostEqual(0, e.evaluate(), 15)

    def test_evaluate_cos90_expression_in_degrees(self):
        e = Expression('cos(radians(90))')
        self.assertAlmostEqual(0, e.evaluate(), 15)

    def test_evaluate_tan0_expression(self):
        e = Expression('tan(0)')
        self.assertEqual(0, e.evaluate())

    def test_evaluate_tan45_expression_in_radians(self):
        e = Expression('tan(pi/4)')
        self.assertAlmostEqual(1, e.evaluate(), 15)

    def test_evaluate_tan45_expression_in_degrees(self):
        e = Expression('tan(radians(45))')
        self.assertAlmostEqual(1, e.evaluate(), 15)

    def test_evaluate_tan90_expression_in_degrees(self):
        e = Expression('tan(radians(90))')
        self.assertAlmostEqual(math.tan(math.pi/2), e.evaluate(), 15)

    def test_evaluate_factorial_expression(self):
        e = Expression('0!')
        self.assertEqual(1, e.evaluate())

    def test_evaluate_factorial_expression2(self):
        e = Expression('1!')
        self.assertEqual(1, e.evaluate())

    def test_evaluate_factorial_expression3(self):
        e = Expression('5!')
        self.assertEqual(120, e.evaluate())

    def test_evaluate_addition_expression_with_variable(self):
        e = Expression('x+1')
        e.assign_value('x', 1)
        self.assertEqual(2, e.evaluate())

    def test_evaluate_expression_with_multiple_variables(self):
        e = Expression('x+y')
        e.assign_value('x', 1)
        e.assign_value('y', 2)
        self.assertEqual(3, e.evaluate())

    def test_evaluate_expression_with_multiple_ocurrences_of_same_variable(self):
        e = Expression('x*x')
        e.assign_value('x', 10)
        self.assertEqual(100, e.evaluate())

    def test_evaluate_with_parentheses(self):
        e = Expression('((1)+(2))*3')
        self.assertEqual(9, e.evaluate())

    def test_evaluate_long_expression(self):
        e = Expression('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3')
        self.assertEqual(3.0001220703125, e.evaluate())

    def test_evaluate_long_expression2(self):
        e = Expression('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3')
        self.assertEqual(3.0001220703125, e.evaluate())

    def test_evaluate_raises_unassigned_variable_error(self):
        e = Expression('x')
        with self.assertRaises(UnassignedVariable) as _:
            e.evaluate()

    def test_evaluate_raises_unassigned_variable_error_after_reset(self):
        e = Expression('x')
        e.assign_value('x', 42)
        e.evaluate()
        e.reset_variables()
        with self.assertRaises(UnassignedVariable) as _:
            e.evaluate()

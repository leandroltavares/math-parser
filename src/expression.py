from tokenizer import Tokenizer, Value, Variable, Function, Operator, Constant, OpenParentheses, CloseParentheses
from errors import UnassignedVariable


class Expression:
    def __init__(self, expression):
        self.tokenizer = Tokenizer()
        self.tokens, self.variables = self.tokenizer.tokenize(expression)
        self.reset_variables()
        self.rpn = self._convert_to_rpn()

    def _convert_to_rpn(self):
        queue = []
        stack = []
        for token in self.tokens:
            if isinstance(token, (Value, Variable, Constant)):
                queue.append(token)
            if isinstance(token, (OpenParentheses, Function)):
                stack.append(token)
            if isinstance(token, Operator):
                while stack and isinstance(stack[-1], Operator) and \
                        self._has_operator_higher_precedence(token, stack[-1]):
                    queue.append(stack.pop())
                stack.append(token)
            if isinstance(token, CloseParentheses):
                while not isinstance(stack[-1], OpenParentheses):
                    queue.append(stack.pop())
                stack.pop()  # Discard open parentheses
        while stack:
            queue.append(stack.pop())
        return queue

    @staticmethod
    def _has_operator_higher_precedence(token, top):
        return (top.precedence > token.precedence or
                (top.precedence == token.precedence and top.associativity == 'left')
                and not isinstance(top, OpenParentheses))

    def evaluate(self):
        self._ensure_variables_assigned()
        stack = []
        for token in self.rpn:
            if isinstance(token, (Operator, Function)):
                operands = stack[-token.operands_count:]
                del stack[-token.operands_count:]
                stack.append(token.function(*operands))
            if isinstance(token, (Value, Constant)):
                stack.append(float(token.value))
            if isinstance(token, Variable):
                stack.append(self.variables[token.symbol])
        return stack[0]

    def _ensure_variables_assigned(self):
        unassigned_variables = [k for k, v in self.variables.items() if not v]
        if unassigned_variables:
            raise UnassignedVariable(str(unassigned_variables))

    def assign_value(self, variable, value):
        self.variables[variable] = value

    def reset_variables(self):
        self.variables = dict.fromkeys(self.variables, None)

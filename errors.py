class UnmatchingCloseParentheses(Exception):
    def __init__(self, position):
        self.position = position


class UnmatchingOpenParentheses(Exception):
    pass


class UnexpectedCharacter(Exception):
    def __init__(self, position):
        self.position = position


class UnassignedVariable(Exception):
    def __init__(self, variable_name):
        self.variable_name = variable_name

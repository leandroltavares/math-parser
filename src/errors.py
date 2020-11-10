class UnmatchingCloseParentheses(Exception):
    def __init__(self, position):
        super().__init__()
        self.position = position


class UnmatchingOpenParentheses(Exception):
    pass


class UnexpectedCharacter(Exception):
    def __init__(self, position):
        super().__init__()
        self.position = position


class UnassignedVariable(Exception):
    def __init__(self, variable_name):
        super().__init__()
        self.variable_name = variable_name

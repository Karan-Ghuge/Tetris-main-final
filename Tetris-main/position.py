class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __add__(self, other):
        return Position(self.row + other.row, self.column + other.column)

    def __repr__(self):
        return f"({self.row}, {self.column})"

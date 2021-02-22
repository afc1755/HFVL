# queue node used in BFS
class Node:
    # `(x, y)` represents coordinates of a cell in the matrix
    # maintain a parent node for the printing path
    def __init__(self, x, y, parent, score):
        self.x = x
        self.y = y
        self.parent = parent
        self.score = score

    def __repr__(self):
        return str((self.x, self.y))

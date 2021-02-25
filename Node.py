# queue node used in BFS
class Node:
    # `(x, y)` represents coordinates of a cell in the matrix
    # maintain a parent node for the printing path
    def __init__(self, x, y, parent, score, visited):
        self.x = x
        self.y = y
        self.parent = parent
        self.score = score
        self.visited = visited

    def __repr__(self):
        return str((self.x, self.y))

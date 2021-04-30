# queue node used in BFS for Hash Function Visualization
# created by Andrew Chabot
# RIT Master's Project 2021


class Node:
    # (x, y) represents coordinates of the cell in the frame's matrix
    # maintain a parent node for re-tracing path back through to arrow
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent

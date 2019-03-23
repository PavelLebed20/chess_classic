#################################################
# MODULE: Vector and move classes implementation#
# AUTHOR: Fedorov Dmitrii                       #
# LAST UPDATE: 03/03/2019                       #
#################################################


class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


class Move:
    def __init__(self, point_from, point_to):
        self.point_from = point_from
        self.point_to = point_to

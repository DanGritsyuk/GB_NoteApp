class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def GetDistance(point1, point2):
        return ((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2) ** (0.5)

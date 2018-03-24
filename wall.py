import math
import matplotlib.pyplot as plt


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.x2, self.y1, self.y2=x1,x2,y1,y2
        self.length = math.hypot(x2 - x1, y2 - y1)

    def getEndian(self):
        return [[self.x1, self.y1], [self.x2, self.y2]]

    def getPolarEndian(self, center=None):
        x1, x2, y1, y2 = self.x1, self.x2, self.y1, self.y2
        if center != None:
            x1, x2, y1, y2 = x1 - center[0], x2 - center[0], y1 - center[1], y2 - center[1]

        def convert(x, y):
            angle=math.atan2(y, x)
            while angle < 0:
                angle+=math.pi*2
            return [angle, math.hypot(x, y)]

        return [convert(x1, y1), convert(x2, y2)]

    def plot(self):
        plt.plot([self.x1, self.x2], [self.y1, self.y2], color='black')

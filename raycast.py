
from wall import *

class RaycastReceiver:

    def __init__(self, block : Wall, center=None):
        self.bind(block, center)


    def bind(self, wall : Wall, center=None):
        self.wall = wall
        beginEndian, endEndian = wall.getPolarEndian(center)

        if center==None:
            center=(0,0)
        self.center=center
        v1x, v1y=wall.x1-center[0], wall.y1-center[1]
        v2x, v2y=wall.x2-wall.x1, wall.y2-wall.y1
        self.isFront= v1x*v2y - v1y*v2x >0


        if endEndian[0]<beginEndian[0]:
            beginEndian, endEndian=endEndian, beginEndian

        if endEndian[0]-beginEndian[0] > math.pi:
            endEndian[0]-=math.pi*2
            beginEndian, endEndian = endEndian, beginEndian

        self.beginEndian=beginEndian
        self.endEndian=endEndian
        self.viewAngle= endEndian[0] - beginEndian[0]
        self.viewAngle_sin=math.sin(self.viewAngle)
        self.viewRightAngle_sin=max(min(endEndian[1] * self.viewAngle_sin / wall.length, 1), -1)
        self.viewRightAngle=math.asin(self.viewRightAngle_sin)
        isSharp= endEndian[1] ** 2 - beginEndian[1] ** 2 - wall.length ** 2 > 0

        if isSharp:
            self.viewRightAngle=min(self.viewRightAngle, math.pi - self.viewRightAngle)
        else:
            self.viewRightAngle = max(self.viewRightAngle, math.pi - self.viewRightAngle)


    def getCastDepth(self, angle:float, maxdist=1000):
        if (angle-self.beginEndian[0])%(math.pi * 2)>self.endEndian[0]-self.beginEndian[0]:
            return maxdist
        angle-=self.beginEndian[0]
        hitangle= self.viewRightAngle - angle
        return self.viewRightAngle_sin * self.beginEndian[1] / math.sin(hitangle)

    def getCastDepthBuffer(self, startAngle, endAngle, bufsize, maxDist=1000):
        pass


class Raycast:

    def __init__(self, receiverList: list):
        self.receiverList=receiverList
        self.center=(0,0)

    def setCenter(self, center):
        self.center=center
        for r in self.receiverList:
            r.bind(r.wall, center)

    def getCastDepth(self, rayDirectionAngle:float, maxdist=1000):
        return min([c.getCastDepth(rayDirectionAngle, maxdist) for c in self.receiverList])




if __name__=="__main__":
    import matplotlib.pyplot as plt
    blocks=[
        Wall(4, 0, 4, 2),
        Wall(4, 2, 8, 2),
        Wall(8, 2, 8, 4),
        Wall(8, 4, 8, 20),
        Wall(8, 20, -20, 20),
        Wall(-20, 20, -20, -20),
        Wall(-20, -20, 20, -20),
        Wall(20, -20, 20, 20),
    ]
    m=Raycast([RaycastReceiver(b) for b in blocks])
    m.setCenter((0, -10))
    for i in range(3600):
        angle=i*math.pi/1800
        d=m.getCastDepth(angle, 32)
        plt.plot([m.center[0],m.center[0]+d*math.cos(angle)], [m.center[1], m.center[1]+d*math.sin(angle)], color='gray')

    for b in blocks:
        b.plot()
    plt.show()


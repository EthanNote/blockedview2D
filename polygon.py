
from raycast import *
from wall import *
import matplotlib.pyplot as plt


class Polygon:
    def __init__(self, vertices):
        self.receivers=[]
        self.plotXY=[[],[]]
        if len(vertices)<2:
            return

        last=vertices[-1]
        self.plotXY[0].append(last[0])
        self.plotXY[1].append(last[1])
        if len(last)!=2:
            pass

        for v in vertices:
            if len(v)!=2:
                pass

            self.receivers.append(RaycastWallReceiver(Wall(last[0], last[1], v[0], v[1])))
            self.plotXY[0].append(v[0])
            self.plotXY[1].append(v[1])
            last=v

    def plot(self):
        plt.plot(self.plotXY[0], self.plotXY[1], color='black')

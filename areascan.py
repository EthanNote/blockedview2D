from polygon import Polygon, RaycastMultiPolygonReceiver
import numpy as np
import math
class AreaScan:
    def __init__(self, receiver):
        self.posmap=dict()
        self.receiver=receiver
        self.maxvalue=0

    def getMap(self, xstart, xend, ystart, yend, step):
        xs=[]
        ys=[]
        cs=[]
        i=xstart
        while i<=xend:
            j=ystart
            while j<=yend:
                self.receiver.bind(self.receiver.polygons, [i, j])
                buf=self.receiver.getCircleDepthBuffer()
                area=0
                if max(buf)<100:
                    area=sum([d*d for d in buf])
                    xs.append(i)
                    ys.append(j)
                    cs.append(area)
                j+=step

            i+=step

        return xs, ys, cs


if __name__=="__main__":
    import matplotlib.pyplot as plt
    import json
    data=json.load(open('polygon.json'))
    P=[ Polygon(p['vertices']) for p in data['polygons'] ]

    plt.scatter([2], [1])
    m = RaycastMultiPolygonReceiver()
    m.bind(P,[0,0])
    #print(m.polygons)
    scan=AreaScan(m)
    xs, ys, cs =scan.getMap(-1,10,-1,8, 0.1)
    plt.scatter(xs, ys, c=cs)

    for p in P:
        p.plot()

    plt.show()
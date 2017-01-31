from TopologyFunctionality.Octree.Point import Point
from TopologyFunctionality.Octree.OctreeBin import OctreeBin
from TopologyFunctionality.Octree.Bounds import Bounds

def getPointObjects(x,y):
	pointObjs = []
	for idx in range(x.size):
		a=x[idx]
		b=y[idx]
		newObj = Point(a,b,0)
		pointObjs.append(newObj)
	return pointObjs
	
def getSubTrajectory(bin1,bin2,point1,point2):
        xPlane, yPlane, zPlane = bin1.dimensionsShared(bin2)
        delt = [point1.X - point2.X, point1.Y - point2.Y, point1.Z - point2.Z]
        initPt = [point1.X,point1.Y,point1.Z]
        times = []
        numTimes = 0
        if xPlane is not None and delt[0] != 0:
                xt = (xPlane - initPt[0])/delt[0]
                times.append(xt)
        if yPlane is not None and delt[1] != 0:
                yt = (yPlane - initPt[1])/delt[1]
                times.append(yt)
        if zPlane is not None  and delt[2] != 0:
                zt = (zPlane - initPt[2])/delt[2]
                times.append(zt)
        midTimes = []
        extraPts = []
        times.sort()
        for i in range(len(times)-1):
                midTime = (times[i] + times[i+1])/2
                if midTime == times[i]:
                        continue
                x = initPt[0] + delt[0]*midTime
                y = initPt[1] + delt[1]*midTime
                z = initPt[2] + delt[2]*midTime
                extraPts.append(Point(x,y,z))
        return extraPts
                
        
                        
                

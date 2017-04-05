from TopologyFunctionality.Octree.Point import Point
from TopologyFunctionality.Octree.OctreeBin import OctreeBin
from TopologyFunctionality.Octree.Bounds import Bounds
from TopologyFunctionality.Octree.TrajectorySegment import TrajectorySegment
import pdb

def getPointObjects(x,y):
	pointObjs = []
	for idx in range(x.size):
		a=x[idx]
		b=y[idx]
		newObj = Point(a,b,0)
		pointObjs.append(newObj)
	return pointObjs

def getPointObject(x,y):
	pointObjs = []
	return Point(x,y,0)

def copyPointObjects(points):
        retPts = []
        for point in points:
                retPts.append(Point(point.X,point.Y,point.Z))
        return retPts

def getPointObsFromSingleSrc(points):
        pointObjs = []
        for x,y in points:
                pointObjs.append(Point(float(x),float(y),0))
        return pointObjs
	
def getSubTrajectory(bin1,bin2,point1,point2):
        xPlane, yPlane, zPlane = bin1.dimensionsShared(bin2)
        delt = [point2.X - point1.X, point2.Y - point1.Y, point2.Z - point1.Z]
        initPt = [point1.X,point1.Y,point1.Z]
        times = []
        numTimes = 0
        if len(xPlane)!=0 and delt[0] != 0:
                for plane in xPlane:
                        xt = (plane - initPt[0])/delt[0]
                        if 0 < xt < 1:
                                times.append(xt)
        if len(yPlane)!=0 and delt[1] != 0:
                for plane in yPlane:
                        yt = (plane - initPt[1])/delt[1]
                        if 0 < yt < 1:
                                times.append(yt)
        if len(zPlane)!=0  and delt[2] != 0:
                for plane in zPlane:
                        zt = (plane - initPt[2])/delt[2]
                        if 0 < zt < 1:
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

def getBin(firstBin, binNos):
        currBin = firstBin
        for binNo in binNos:
                if currBin.children == []:
                        pdb.set_trace()
                currBin = currBin.children[binNo]
        return currBin

def getTempPtBin(firstBin,binNos,exPt):
        currBin = firstBin
        for binNo in binNos:
                if currBin.children:
                        currBin = currBin.children[binNo]
        while currBin.children:
                binIdx = currBin.findIndex(exPt)
                currBin = currBin.children[binIdx]
        return currBin

def addTrajToBinPath(firstBin,point1,point2):
        currBin = firstBin
        i=0
        point2binlen = len(point2.binPath)
        minLen = min(len(point1.binPath),point2binlen)
        while point1.binPath[i] == point2.binPath[i]:
                currBin = currBin.children[point1.binPath[i]]
                i=i+1
                if i == minLen:
                        break
        if i != point2binlen:
                for j in range(i,point2binlen):
                        currBin = currBin.children[point2.binPath[j]]
                        currBin.incrementTrajectoryCount()

def removeTrajFromBinPath(firstBin,point1,point2):
        currBin=firstBin
        i=0
        point2binlen = len(point2.binPath)
        minLen = min(len(point1.binPath),point2binlen)
        while point1.binPath[i] == point2.binPath[i]:
                currBin = currBin.children[point1.binPath[i]]
                i=i+1
                if i==minLen:
                        break
        if i != point2binlen:
                for j in range(i,point2binlen):
                        currBin = currBin.children[point2.binPath[j]]
                        currBin.decrementTrajectoryCount()

def getFirstLevelBin(anyBin):
        while anyBin.parent:
                anyBin=anyBin.parent
        return anyBin
        

def addTrajectory(point1, point2, bin1, bin2):
        extraPts = getSubTrajectory(bin1,bin2,point1,point2)
        addExtraPointsToBins(point1,point2,extraPts,getFirstLevelBin(bin1))
        traj = TrajectorySegment(point1,point2,extraPts)
        addTrajToBinPath(getFirstLevelBin(bin1),point1,point2)


def addExtraPointsToBins(point1,point2,extraPts,firstBin):
        for point in extraPts:
                currBin = syncExtraPointWithBin(point,firstBin)
                closestRelative = point.findClosestRelative([point1,point2])
                addTrajToBinPath(getFirstLevelBin(currBin),closestRelative,point)

def syncExtraPointWithBin(point,firstBin):
        currBin = firstBin
        while len(currBin.children)!=0:
                idx = currBin.findIndex(point)
                point.addToBinPath([idx])
                currBin = currBin.children[idx]
        return currBin

def syncNewPointWithBin(point,firstBin,lastPt):
        currBin,binPath = getRelaxedBinAndBinPath(firstBin,point,lastPt)
        point.binPath = binPath
        currBin.addPoints([point])
        return currBin

def getRelaxedBinAndBinPath(firstBin,point,lastPt):
        currBin = firstBin
        binPath = []
        i=0
        checkLastPt=True
        while len(currBin.children)!=0:
                idx = currBin.findIndex(point)
                if i<len(lastPt.binPath):
                        if idx != lastPt.binPath[i] and checkLastPt:
                                if getBin(firstBin,lastPt.binPath[:i+1]).relaxedContent(point):
                                        idx = lastPt.binPath[i]
                                else:
                                        checkLastPt=False
                binPath.append(idx)
                currBin = currBin.children[idx]
                i+=1
        return currBin,binPath

def incrementExtraPointBins(exPt,firstBin,neighbors):
        exPt.binPath = updateTempPointBinPath(exPt, firstBin)
        closestRelative = exPt.findClosestRelative(neighbors)
        exPtBinLen = len(exPt.binPath)
        minLen = min(len(closestRelative.binPath),exPtBinLen)
        i=0
        currBin = firstBin
        while exPt.binPath[i] == closestRelative.binPath[i]:
                currBin = currBin.children[exPt.binPath[i]]
                i=i+1
                if i == minLen:
                        break
        if i != exPtBinLen:
                for j in range(i,exPtBinLen):
                        currBin = currBin.children[exPt.binPath[j]]
                        currBin.incrementTrajectoryCount()
        return currBin

def updateTempPointBinPath(exPt,firstBin):
        currBin = firstBin
        newPath = []
        for binNo in exPt.binPath:
                if currBin.children:
                        currBin = currBin.children[binNo]
                        newPath.append(binNo)
        while currBin.children:
                binIdx = currBin.findIndex(exPt)
                currBin = currBin.children[binIdx]
                newPath.append(binIdx)
        return newPath

def getChildPtCount(parent):
        childpts = 0
        for child in parent.children:
                if len(child.children)!=0:
                        childpts = childpts + getChildPtCount(child)
                else:
                        childpts = childpts + len(child.points)
        return childpts

from .Bounds import Bounds
from .OctreeBin import OctreeBin
from .TrajectorySegment import TrajectorySegment
from TopologyFunctionality.Helper.OctreeUtil import *

class Octree(object):

    def __init__(self, minDepth):
        self.firstLevel = []
        self.bounds = []
        self.points = []
        self.minDepth = minDepth

    def appendPoints(self, points):
        lastPoint = self.points[-1]
        self.createTrajectories(lastPoint,points,1)
        self.points.extend(points)
        removal =  self.points[0:len(points)]
        for point in removal:
            newBin = self.getBin(point.binPath)
            newBin.removePoint(point)
            newBin.trajCt = newBin.trajCt-1
            for traj in point.trajectories:
                traj.killTrajectory(self)
        del self.points[0:len(points)]


    def prependPoints(self, points):
        lastPoint = self.points[0]
        self.createTrajectories(lastPoint,points,1)
        removal = self.points[-len(points):]
        for point in removal:
            newBin = self.getBin(point.binPath)
            newBin.removePoint(point)
            newBin.trajCt = newBin.trajCt-1
            for traj in point.trajectories:
                traj.killTrajectory(self)
        del self.points[-len(points):]
        points.extend(self.points)
        self.points = points

    def createOctree(self, points, is2D):
        self.points = points
        minX = float('inf')
        minY = float('inf')
        minZ = float('inf')
        maxX = float('-inf')
        maxY = float('-inf')
        maxZ = float('-inf')
        for point in points:
            if point.X < minX:
                minX = point.X
            if point.Y < minY:
                minY = point.Y
            if point.Z < minZ:
                minZ = point.Z
            if point.X > maxX:
                maxX = point.X
            if point.Y > maxY:
                maxY = point.Y
            if point.Z > maxZ:
                maxZ = point.Z
        if is2D:
            minZ = minZ-1
            maxZ = maxZ+1
        else:
            zDist = maxZ - minZ
            maxZ = maxZ + (zDist/2)
            minZ = minZ - (zDist/2)
        xDist = maxX - minX
        maxX = maxX + (xDist/2)
        minX = minX - (xDist/2)
        yDist = maxY - minY
        maxY = maxY + (yDist/2)
        minY = minY - (yDist/2)
        self.bounds = Bounds(minX,minY,minZ,maxX,maxY,maxZ)
        self.firstLevel = OctreeBin(None, self.points, self.bounds,1,0)
        self.splitBin(self.firstLevel)
        lastPoint = self.points[0]
        self.createTrajectories(lastPoint, points[1:],0)

    def createTrajectories(self,lastPoint,points,isSyncWithBin):
        for point in points:
            if isSyncWithBin:
                self.syncNewPointWithBin(point)
            bin1 = self.getBin(lastPoint.binPath)
            bin2 = self.getBin(point.binPath)
            if bin1 != bin2:
                self.addTrajectory(point, lastPoint,bin2,bin1)
            lastPoint=point
        

    def splitBin(self,newBin):
        if len(newBin.points) >= 2 and newBin.depth < self.minDepth:
            newBin.divide()
            for child in newBin.children:
                self.splitBin(child)

    def drawBins(self, newBin):
        if len(newBin.children)==0:
            print(newBin.trajCt)
            return [(newBin.bounds, newBin.trajCt/80)]
        else:
            binFacts = []
            for child in newBin.children:
                binFacts.extend(self.drawBins(child))
            return binFacts

    def getBin(self, binNos):
        currBin = self.firstLevel
        for binNo in binNos:
            currBin = currBin.children[binNo]
        return currBin

    def syncNewPointWithBin(self,point):
        currBin = self.firstLevel
        while len(currBin.children)!=0:
            idx = currBin.findIndex(point)
            point.addToBinPath([idx])
            currBin = currBin.children[idx]
        currBin.addPoints([point])
        return currBin

    def addTrajectory(self, point1, point2, bin1, bin2):
        extraPts = getSubTrajectory(bin1,bin2,point1,point2)
        extraBins = self.addExtraPointsToBins(extraPts)
        traj = TrajectorySegment(point1,point2,extraPts)
        bin2.trajCt = bin2.trajCt+1

    def addExtraPointsToBins(self,extraPts):
        for point in extraPts:
            currBin = self.syncNewPointWithBin(point)
            currBin.trajCt = currBin.trajCt+1

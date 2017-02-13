from .Bounds import Bounds
from TopologyFunctionality.Helper.OctreeUtil import *
from TopologyFunctionality.Helper import OctreeUtil as ou
import pdb

class OctreeBin(object):

    #Children always stored so binary search works as:
    #is greater than zMid, is greater than yMid, is greather than xMid
    #if true, lies to right else to left, greater for all at index 7. Less for all at index 0

    def __init__(self, parent, points, bounds,depth, trajCt):
        self.children = []
        self.points = points
        self.parent = parent
        self.bounds = bounds
        self.depth = depth
        self.trajCt = trajCt
        self.arePointsSorted = True

    def __repr__(self):
        return "min: x:%f y:%f z:%f / max: x:%f y:%f z:%f" % (self.bounds.minX,self.bounds.minY,self.bounds.minZ,self.bounds.maxX,self.bounds.maxY,self.bounds.maxZ)
                
    def divide(self):
        for i in range(8):
            childBound = self.bounds.getChild(i)
            pts=[]
            newChild = OctreeBin(self,pts,childBound, self.depth+1,0)
            self.children.append(newChild)
        if not self.arePointsSorted:
            self.sortPoints()
        prevPointId=-10
        firstLvl = ou.getFirstLevelBin(self)
        for ptIdx,point in enumerate(self.points):
            binIdx = self.findIndex(point)
            self.children[binIdx].addPoints([point])
            point.addToBinPath([binIdx])
            if point.pointId-prevPointId==1: 
                bin1 = ou.getBin(firstLvl,self.points[ptIdx-1].binPath)
                bin2 = ou.getBin(firstLvl,point.binPath)
                notContainedinTraj = True
                #if the point contains a traj, check to see if other point is in traj.
                #if so, then don't create a new one, just increment point's bin's ct
                if point.trajectories:
                    for traj in point.trajectories:
                        if traj.contains(self.points[ptIdx-1]):
                            notContainedinTraj=False
                            bin2.incrementTrajectoryCount()
                            for extraPt in traj.tempPoints:
                                exBin = ou.incrementExtraPointBins(extraPt,firstLvl,[point, self.points[ptIdx-1]])
                if bin1 != bin2 and notContainedinTraj:
                    ou.addTrajectory(self.points[ptIdx-1],point,bin1,bin2)
            #the point has to have a neighbor in another binset
            else:
                for traj in point.trajectories:
                    for extraPt in traj.tempPoints:
                        if extraPt.binPath[:self.depth-1] == point.binPath[:self.depth-1]:
                            exBin = ou.incrementExtraPointBins(extraPt,firstLvl,[point, self.points[ptIdx-1]])
                myBin = ou.getBin(firstLvl,point.binPath)
                myBin.incrementTrajectoryCount()
            prevPointId=point.pointId
        self.points=[]

    def sortPoints(self):
        self.points.sort()
        self.arePointsSorted=True

    def mergeChildren(self):
        self.arePointsSorted=False
        for child in self.children:
            child.mergeChildren()
            for point in child.points:
                for traj in point.trajectories:
                    if traj.front.binPath[:self.depth] == traj.back.binPath[:self.depth]:
                        traj.killTrajectory(self)
                point.shortenBinPath(1)
            self.points.extend(child.points)
            child.points = []
        del self.children[:]

    def addPoints(self, points):
        self.points.extend(points)

    def removePoint(self,point):
        if point not in self.points:
            pdb.set_trace()
        self.points.remove(point)

    def findIndex(self,point):
        idx=0
        if(point.Z > self.bounds.midZ):
            idx=4
        if(point.Y > self.bounds.midY):
            idx = idx + 2
        if(point.X > self.bounds.midX):
            idx = idx + 1
        return idx

    def dimensionsShared(self,compBin):
        #Important to note that the bins of adjacent points must be adjacent
        if self.depth == compBin.depth:
            if self.bounds.midX == compBin.bounds.midX:
                xPlane = []
            elif self.bounds.midX > compBin.bounds.midX:
                xPlane = [self.bounds.minX]
            else:
                xPlane = [self.bounds.maxX]

            if self.bounds.midY == compBin.bounds.midY:
                yPlane = []
            elif self.bounds.midY > compBin.bounds.midY:
                yPlane = [self.bounds.minY]
            else:
                yPlane = [self.bounds.maxY]

            if self.bounds.midZ == compBin.bounds.midZ:
                zPlane = []
            elif self.bounds.midZ > compBin.bounds.midZ:
                zPlane = [self.bounds.minZ]
            else:
                xPlane = [self.bounds.maxZ]
        else:
            if self.depth < compBin.depth:
                xPlane = [self.bounds.minX, self.bounds.maxX]
                yPlane = [self.bounds.minY, self.bounds.maxY]
                zPlane = [self.bounds.minZ, self.bounds.maxZ]
            else:
                xPlane = [compBin.bounds.minX, compBin.bounds.maxX]
                yPlane = [compBin.bounds.minY, compBin.bounds.maxY]
                zPlane = [compBin.bounds.minZ, compBin.bounds.maxZ]
    
        return xPlane, yPlane, zPlane

    def checkAncestorsTraj(self):
        if self.parent is not None:
            return self.parent.isTrajDecreasing(self.trajCt)
        else:
            return True

    def isTrajDecreasing(self, trajCt):
        if self.parent is not None:
            return self.parent.isTrajDecreasing(self.trajCt) and self.trajCt >= trajCt
        else:
            return True

    def incrementTrajectoryCount(self):
        self.trajCt = self.trajCt+1

    def decrementTrajectoryCount(self):
        self.trajCt = self.trajCt-1

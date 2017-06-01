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
        for point in points:
            point.lowestBin = self
        self.parent = parent
        self.bounds = bounds
        self.depth = depth
        self.trajCt = trajCt
        self.relaxedEpsilon = 0.05

    def __repr__(self):
        return "min: x:%f y:%f z:%f / max: x:%f y:%f z:%f" % (self.bounds.minX,self.bounds.minY,self.bounds.minZ,self.bounds.maxX,self.bounds.maxY,self.bounds.maxZ)
                
    def divide(self):
        for i in range(8):
            childBound = self.bounds.getChild(i)
            pts=[]
            newChild = OctreeBin(self,pts,childBound, self.depth+1,0)
            self.children.append(newChild)
        prevPoint=None
        for ptIdx,point in enumerate(self.points):
            if point.prev==prevPoint and prevPoint!=None:
                bin2 = ou.getRelaxedBin(point,prevPoint)
                point.lowestBin = bin2
                bin2.addPoints([point])
                bin1 = prevPoint.lowestBin
                notContainedinTraj = True
                #if the point contains a traj, check to see if other point is in traj.
                #if so, then don't create a new one, just increment point's bin's ct
                if point.trajectories:
                    for traj in point.trajectories:
                        if traj.contains(prevPoint):
                            notContainedinTraj=False
                            bin2.incrementTrajectoryCount()
                            for extraPt in traj.tempPoints:
                                ou.incrementExtraPointBins(extraPt)
                if bin1 != bin2 and notContainedinTraj:
                    ou.introduceTrajectory(prevPoint,point,bin1,bin2)
            #the point has to have a neighbor in another binset
            else:
                binIdx = self.findIndex(point)
                receivingBin = self.children[binIdx]
                receivingBin.addPoints([point])
                point.updateBin(receivingBin)
                for traj in point.trajectories:
                    for extraPt in traj.tempPoints:
                        if extraPt.lowestBin == point.lowestBin.parent:
                            ou.incrementExtraPointBins(extraPt)
                myBin = point.lowestBin
                myBin.incrementTrajectoryCount()
            prevPoint=point
        self.points=[]

    def mergeChildren(self):
        for child in self.children:
            child.mergeChildren()
            for point in child.points:
                for traj in point.trajectories:
                    if traj.front.lowestBin.parent == traj.back.lowestBin.parent:
                        traj.killTrajectory(self)
                point.updateBinToParent()
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
            return self.parent.checkAncestorsTraj() and self.trajCt >=2
        else:
            return True

    def relaxedContent(self,point):
        mybounds = self.bounds
        withinX = (mybounds.maxX + self.relaxedEpsilon)>=point.X>=(mybounds.minX - self.relaxedEpsilon)
        withinY = (mybounds.maxY + self.relaxedEpsilon)>=point.Y>=(mybounds.minY - self.relaxedEpsilon)
        withinZ = (mybounds.maxZ + self.relaxedEpsilon)>=point.Z>=(mybounds.minZ - self.relaxedEpsilon)
        return withinX and withinY and withinZ

    def incrementTrajectoryCount(self):
        self.trajCt = self.trajCt+1

    def decrementTrajectoryCount(self):
        self.trajCt = self.trajCt-1
        
    def matchBinDepths(self,yourBin):
        myBin = self
        while myBin.depth > yourBin.depth:
                myBin = myBin.parent
        while myBin.depth < yourBin.depth:
            yourBin = yourBin.parent
        return myBin,yourBin

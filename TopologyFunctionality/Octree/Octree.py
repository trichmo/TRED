from .Bounds import Bounds
from .OctreeBin import OctreeBin
from .TrajectorySegment import TrajectorySegment
from TopologyFunctionality.Helper.OctreeUtil import *
import pdb

class Octree(object):

    def __init__(self, minDepth):
        self.firstLevel = []
        self.bounds = []
        self.points = []
        self.minDepth = minDepth
        #self.extraPts = []
        self.splitPtThresh = 0.6

    def appendPoints(self, points):
        lastPoint = self.points[-1]
        self.handleBinEnds(self.points[0],self.points[len(points)])
        self.createTrajectories(lastPoint,points,1)
        self.points.extend(points)
        removal =  self.points[0:len(points)]
        self.killPoints(removal)
        del self.points[0:len(points)]


    def prependPoints(self, points):
        lastPoint = self.points[0]
        revPoints = points[::-1]
        self.createTrajectories(lastPoint,revPoints,1)
        self.handleBinEnds(lastPoint,points[0])
        removal = self.points[-len(points):]
        self.killPoints(removal)
        del self.points[-len(points):]
        points.extend(self.points)
        self.points = points

    def handleBinEnds(self,oldFirst,newFirst):
        oldBinTraj = getBin(self.firstLevel,oldFirst.binPath)
        oldBinTraj.decrementTrajectoryCount()
        newBinTraj = getBin(self.firstLevel,newFirst.binPath)
        newBinTraj.incrementTrajectoryCount()

    def killPoints(self, removal):
        for point in removal:
            for traj in point.trajectories:
                #only for drawing
                #for pt in traj.tempPoints:
                    #self.extraPts.remove(pt)
                traj.killTrajectory(self.firstLevel)   
            editBin = getBin(self.firstLevel,point.binPath)
            editBin.removePoint(point)
            self.manageBinMerge(editBin)

    def manageBinMerge(self, editedBin):
        editedParent = editedBin.parent
        if (editedParent.trajCt == 0 or not editedBin.checkAncestorsTraj()) and editedBin.depth>2:
            #pdb.set_trace()
            editedParent.mergeChildren()
            self.manageBinMerge(editedParent)

        
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
        self.initializeSplitting()

    def createTrajectories(self,lastPoint,points,isSyncWithBin):
        for point in points:
            if isSyncWithBin:
                syncNewPointWithBin(point,self.firstLevel)
            bin1 = getBin(self.firstLevel,lastPoint.binPath)
            bin2 = getBin(self.firstLevel,point.binPath)
            if bin1 != bin2:
                addTrajectory(lastPoint, point,bin1,bin2)
                self.splitBin(bin2)
            lastPoint=point

    def initializeSplitting(self):
        self.firstLevel.divide()
        for child in self.firstLevel.children:
            self.splitBin(child)
        

    def splitBin(self,newBin):
        if ((newBin.trajCt >= 2 and newBin.checkAncestorsTraj()) or
        (len(newBin.points)/len(self.points) > self.splitPtThresh)):
            if newBin.depth < self.minDepth:
                newBin.divide()
                firstBin = getBin(self.firstLevel, self.points[0].binPath)
                if firstBin in newBin.children:
                    firstBin.incrementTrajectoryCount()
                for child in newBin.children:
                    self.splitBin(child)

    def drawBins(self, newBin):
        if len(newBin.children)==0:
            return [(newBin.bounds, newBin.trajCt/15)]
        else:
            binFacts = []
            for child in newBin.children:
                binFacts.extend(self.drawBins(child))
            return binFacts



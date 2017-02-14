from .Bounds import Bounds
from .OctreeBin import OctreeBin
from .TrajectorySegment import TrajectorySegment
from TopologyFunctionality.Helper import OctreeUtil as ou 
import pdb

class Octree(object):

    def __init__(self, minDepth):
        self.firstLevel = []
        self.bounds = []
        self.points = []
        self.minDepth = minDepth
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
        currBin = self.firstLevel
        for binNo in oldFirst.binPath:
            currBin = currBin.children[binNo]
            currBin.decrementTrajectoryCount()
            
        currBin = self.firstLevel
        for binNo in newFirst.binPath:
            currBin = currBin.children[binNo]
            currBin.incrementTrajectoryCount()

    def killPoints(self, removal):
        for point in removal:
            for traj in point.trajectories:
                traj.killTrajectory(self.firstLevel)   
            editBin = ou.getBin(self.firstLevel,point.binPath)
            editBin.removePoint(point)
            self.manageBinMerge(editBin)

    def manageBinMerge(self, editedBin):
        editedParent = editedBin.parent
        if (editedParent.trajCt == 0 or not editedBin.checkAncestorsTraj()) and editedBin.depth>2:
            siblingPts = ou.getChildPtCount(editedParent)
            if self.splitPtThresh>(siblingPts/len(self.points)):
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
                ou.syncNewPointWithBin(point,self.firstLevel,lastPoint)
            bin1 = ou.getBin(self.firstLevel,lastPoint.binPath)
            bin2 = ou.getBin(self.firstLevel,point.binPath)
            if bin1 != bin2:
                ou.addTrajectory(lastPoint, point,bin1,bin2)
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
                for child in newBin.children:
                    self.splitBin(child)

    def drawBins(self, newBin):
        if len(newBin.children)==0:
            return [(newBin.bounds, newBin.trajCt/20)]
        else:
            binFacts = []
            for child in newBin.children:
                binFacts.extend(self.drawBins(child))
            return binFacts


    def getKdSubsamplePoints(self, newBin = None):
        if newBin == None:
            newBin = self.firstLevel
        if len(newBin.children)==0:
            if newBin.trajCt > 2:
                bds = newBin.bounds
                return [[bds.midX,bds.midY]]
            else:
                return []
        else:
            keyBins = []
            for child in newBin.children:
                keyBins.extend(self.getKdSubsamplePoints(child))
            return keyBins


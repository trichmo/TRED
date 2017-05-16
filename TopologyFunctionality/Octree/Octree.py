from .Bounds import Bounds
from .OctreeBin import OctreeBin
from .TrajectorySegment import TrajectorySegment
from TopologyFunctionality.Helper import OctreeUtil as ou 
import pdb

class Octree(object):

    def __init__(self, minDepth, bounds = [], trajThresh=400, trajMax = 800):
        self.trajMax = trajMax
        self.trajThreshold = trajThresh
        self.firstLevel = []
        self.bounds = bounds
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
        if (editedParent.trajCt < self.trajThreshold or not editedParent.checkAncestorsTraj()) and editedBin.depth>=self.trajThreshold:
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
        xDist = maxX - minX
        yDist = maxY - minY
        xCenter = (maxX+minX)/2
        yCenter = (maxY+minY)/2
        if is2D:
            minZ = minZ-1
            maxZ = maxZ+1
            maxDist = max(xDist,yDist)
        else:
            zDist = maxZ - minZ
            maxDist = max(xDist,yDist,zDist)
            zCenter = (maxZ+minZ)/2
            maxZ = zCenter + (maxDist/2)
            minZ = zCenter - (maxDist/2)
        maxX = xCenter + (maxDist/1.5)
        minX = xCenter - (maxDist/1.5)
        maxY = yCenter + (maxDist/1.5)
        minY = yCenter - (maxDist/1.5)
        if self.bounds==[]:
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
        if ((newBin.trajCt >= self.trajThreshold and newBin.checkAncestorsTraj()) or
        (len(newBin.points)/len(self.points) > self.splitPtThresh)):
            if newBin.depth < self.minDepth:
                newBin.divide()
                for child in newBin.children:
                    self.splitBin(child)

    def getDualScaleBins(self,newBin):
        if len(newBin.children)==0:
            isKey = 0
            if newBin.depth == self.minDepth and newBin.trajCt >= self.trajThreshold:
                isKey=1
            return [(newBin.bounds, newBin.trajCt/self.trajMax, isKey)],[]
        else:
            binFacts = []
            checkExtendedFamily=[]
            keyCt = 0 
            for child in newBin.children:
                newFacts,newChecks = self.getDualScaleBins(child)
                keyCt += newFacts[0][2]
                binFacts.extend(newFacts)
                checkExtendedFamily.extend(newChecks)
            if keyCt==0 and newBin.depth == self.minDepth-1:
                if  newBin.trajCt >= self.trajThreshold:
                    binFacts = [(newBin.bounds, newBin.trajCt/self.trajMax, 1)]
                elif newBin.trajCt > 0:
                    checkExtendedFamily = newBin
            return binFacts, checkExtendedFamily

    def drawBins(self, newBin):
        if len(newBin.children)==0:
            isKey = 0
            if newBin.depth == self.minDepth and newBin.trajCt >= self.trajThreshold:
                isKey=1
            return [(newBin.bounds, newBin.trajCt/self.trajMax, isKey)]
        else:
            binFacts = []
            for child in newBin.children:
                binFacts.extend(self.drawBins(child))
            return binFacts


    def getKdSubsamplePoints(self, newBin = None):
        if newBin == None:
            newBin = self.firstLevel
        if len(newBin.children)==0:
            if newBin.trajCt >= self.trajThreshold and newBin.depth == self.minDepth:
                bds = newBin.bounds
                return [[bds.midX,bds.midY]]
            else:
                return []
        else:
            keyBins = []
            for child in newBin.children:
                keyBins.extend(self.getKdSubsamplePoints(child))
            return keyBins

    def compare(self, compOct):
        myBin = self.firstLevel
        binComp = compOct.firstLevel
        return self.compBins(myBin,binComp)

    def compBins(self, myBin,binComp):
        if len(myBin.children) != len(binComp.children):
            print("Something Worse is happening")
            return False
        elif len(myBin.children)==0:
            ct = (myBin.trajCt == binComp.trajCt)
            if ct == False:
                print("Dynamic Count: " , myBin.trajCt)
                print("Static Count: " , binComp.trajCt)
            return ct
        else:
            for idx,child in enumerate(myBin.children):
                temp = self.compBins(child,binComp.children[idx])
                if not temp:
                    return temp
        return True


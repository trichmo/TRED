from .Bounds import Bounds
from .OctreeBin import OctreeBin

class Octree(object):

    def __init__(self, minDepth):
        self.firstLevel = []
        self.bounds = []
        self.points = []
        self.minDepth = minDepth

    def appendPoints(self, points):
        for point in points:
            self.syncNewPointWithBin(point)
        self.points.extend(points)
        removal =  self.points[0:len(points)]
        for point in removal:
            newBin = self.getBin(point.binPath)
            newBin.removePoint(point)
        del self.points[0:len(points)]


    def prependPoints(self, points):
        for point in points:
            self.syncNewPointWithBin(point)
        removal = self.points[-len(points):]
        for point in removal:
            newBin = self.getBin(point.binPath)
            newBin.removePoint(point)
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
        self.firstLevel = OctreeBin(None, self.points, self.bounds,1)
        self.splitBin(self.firstLevel)

    def splitBin(self,newBin):
        if len(newBin.points) >= 2 and newBin.depth < self.minDepth:
            newBin.divide()
            for child in newBin.children:
                self.splitBin(child)

    def drawBins(self, newBin):
        if len(newBin.children)==0:
            return [(newBin.bounds, len(newBin.points)/80)]
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
        

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
            addPointToBinPath(point)
        self.points.extend(points)
        removal =  self.points[0:len(points)]
        for point in removal:
            newBin = getBin(point.binPath[-1])
            newBin.removePoints(point)
        del self.points[0:len(points)]


    def prependPoints(self, points):
        for point in points:
            addPointToBinPath(point)
        removal = self.points[-len(points):]
        for point in removal:
            newBin = getBin(point.binPath[-1])
            newBin.removePoints(point)
        del self.points[-len(points):]
        points.append(self.points)
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
            print(newBin.bounds.minX,newBin.bounds.minY,newBin.bounds.maxX,newBin.bounds.maxY,length(newBin.points))
            return (newBin.bounds.minX,newBin.bounds.minY,newBin.bounds.maxX,newBin.bounds.maxY,length(newBin.points))
        else:
            binFacts = []
            for child in newBin.children:
                binFacts.append(child.drawBins())
            return binFacts

    def getBin(self, binNos):
        currBin = self.firstLevel
        for binNo in binNos:
            currBin = currBin.children[binNo]
        return currBin

    def addPointToBinPath(self,point):
        currBin = self.firstLevel
        while len(currBin.children)!=0:
            idx = currBin.findIndex(point)
            point.addToBinPath([idx])
            currBin = currBin.children[idx]

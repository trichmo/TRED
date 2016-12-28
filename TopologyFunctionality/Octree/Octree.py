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
                        bin = getBin(point.binPath[-1])
                        bin.removePoints(point)
                del self.points[0:len(points)]
                        
	
	def prependPoints(self, points):
                for point in points:
                        addPointToBinPath(point)
                removal = self.points[-len(points):]
                for point in removal:
                        bin = getBin(point.binPath[-1])
                        bin.removePoints(point)
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
		
	def splitBin(self,bin):
		if len(bin.points) >= 2 and bin.depth < self.minDepth:
			bin.divide()
			for child in bin.children:
				self.splitBin(child)
	
	def drawBins(self, bin):
		if len(bin.children)==0:
                        print(bin.bounds.minX,bin.bounds.minY,bin.bounds.maxX,bin.bounds.maxY,length(bin.points))
                        return (bin.bounds.minX,bin.bounds.minY,bin.bounds.maxX,bin.bounds.maxY,length(bin.points))
		else:
                        binFacts = []
                        for child in bin.children:
                                binFacts.append(child.drawBins())
                        return binFacts

        def getBin(self, binNos):
                currBin = self.firstLevel
                for binNo in binNos:
                        currBin = currBin.children[binNo]
                return currBin

        def addPointToBinPath(self,point):
                currBin = self.firstLevel
                while len(currBin.children)~=0:
                        idx = currBin.findIndex(point)
                        point.addToBinPath([idx])
                        currBin = currBin.children[idx]

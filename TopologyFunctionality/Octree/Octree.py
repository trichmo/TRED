class Octree(object):

	def __init__(self, minDepth):
                self.firstLevel = []
		self.bounds = []
		self.points = []
		self.minDepth = minDepth
		
	def appendPoints(self, points):
		self.points.extend(points)
		del self.points[0:len(points)]
	
	def prependPoints(self, points):
		points.extend(self.points)
		del points[self.len(points):]
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
			if point.getX() < minX:
				minX = point.getX()
			if point.getY() < minY:
				minY = point.getY()
			if point.getZ() < minZ:
				minZ = point.getZ()
			if point.getX() > maxX:
				maxX = point.getX()
			if point.getY() > maxY:
				maxY = point.getY()
			if point.getZ() > maxZ:
				maxZ = point.getZ()
				
		if is2D:
			minZ = minZ-1
			maxZ = maxZ+1
		self.bounds = Bounds(minX,minY,minZ,maxX,maxY,maxZ)
		
		bin = OctreeBin(parent, points, bounds,1)
		splitBin(bin)
		
	def splitBin(self,bin):
		if len(bin.points) >= 2 & bin.depth < self.minDepth:
			bin.divide()
			for child in bin.children:
				splitBin(child)
		

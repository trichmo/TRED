class OctreeBin(object):

	#Children always stored so binary search works as:
	#is greater than zMid, is greater than yMid, is greather than xMid
	#if true, lies to right else to left, greater for all at index 7. Less for all at index 0

	def __init__(self, parent, points, bounds,depth):
		self.children = []
		self.points = points
		self.parent = parent
		self.bounds = bounds
		self.depth = depth
		
		
	def divide(self):
		for i in range(8):
			childBound = self.bounds.getChild(i)
			#contains = childBound.containsPoints(self.points)
			#pts=[self.points[idx] for idx in contains]
			pts=[]
			newChild = OctreeBin(self,pts,childBound, self.depth+1)
			self.children.append(newChild)
		for point in self.points:
			idx=0
			if(point.Z > self.bounds.midZ):
				idx=4
			if(point.Y > self.bounds.midY):
				idx = idx + 2
			if(point.X > self.bounds.midX):
				idx = idx + 1
			self.children[idx].addPoints([point])
			point.addToBinPath([idx])
		del self.points[:]
		
	def mergeChildren(self):
		for child in children:
			for point in child.points:
				point.shortenBinPath(1)
			self.points.extend(child.points)
			child.points = []
		del self.children[:]
	
	def addPoints(self, points):
		self.points.extend(points)
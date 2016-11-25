class OctreeBin(object):

	#Children always stored so binary search works as:
	#is greater than zMid, is greater than yMid, is greather than xMid
	#if true, lies to right else to left, greater for all at index 7. Less for all at index 0
	children = property(getChildren, setChildren)
	points = property(getPoints,setPoints)
	parent = propoerty(getParent,setParent)
	bounds = property(getBounds, setBounds)
	depth = property(getDepth, setDepth)

	def __init__(self, parent, points, bounds,depth):
		self.children = []
		self.points = points
		self.parent = parent
		self.bounds = bounds
		self.depth = depth
		
	def setChildren(self, children):
		self._children = children
		
	def getChildren(self):
		return self._children
		
	def setPoints(self, points):
		self._points = points
		
	def addPoints(self, points):
		self._points.extend(points)
		
	def getPoints(self):
		return self._points
		
	def setParent(self, parent):
		self._parent = parent
		
	def getParent(self):
		return self._parent
		
	def setBounds(self, bounds):
		self._bounds = bounds
		
	def getBounds(self):
		return self._bounds
		
	def setBounds(self, depth):
		self._depth = depth
		
	def getDepth(self):
		return self._depth
		
	def divide(self):
		for i in range(8):
			newChild = OctreeBin(self,pts,this.bounds.getChild(i), this.bounds+1)
			self.chidren.extend(newChild)
		for point in self.points:
			idx=0
			if(point.getZ() > bounds.getMidZ()):
				idx=4
			if(point.getY() > bounds.getMidY()):
				idx = idx + 2
			if(point.getX() > bounds.getMidX()):
				idx = idx + 1
			self.children(idx).addPoints(point)
			point.addToBinPath(idx)
		del self.points[:]
		
	def mergeChildren(self):
		for child in children:
			for point in child.points:
				point.shortenBinPath(1)
			self.points.extend(child.points)
			child.points = []
		del self.children[:]
	
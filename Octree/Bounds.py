class Bounds(object):

	minX = property(getMinX, setMinX)
	maxX = property(getMaxX, setMaxX)
	minY = property(getMinY, setMinY)
	maxY = property(getMaxY, setMaxY)
	minZ = property(getMinZ, setMinZ)
	maxZ = property(getMaxZ, setMaxZ)
	midX = property(getMidX, setMidX)
	midY = property(getMidY, setMidY)
	midZ = property(getMidZ, setMidZ)

	def __init__(self, minX, minY, minZ, maxX, maxY, maxZ):
		self._minX = minX
		self._minY = minY
		self._minZ = minZ
		self._maxX = maxX
		self._maxY = maxY
		self._maxZ = maxZ
		self._midX = (maxX - minX)/2
		self._midY = (maxY - minY)/2
		self._midZ = (maxZ - minZ)/2
		
	def containsPoints(self, points):
		contains = []
		for point in points:
			if  >=point.X 
		return contains		
		
	def getMinX(self):
		return self._minX
		
	def setMinX(self, minX):
		self._minX = minX
		
	def getMinY(self):
		return self._minY
		
	def setMinY(self, minY):
		self._minY = minY

	def getMinZ(self):
		return self._minZ
		
	def setMinZ(self, minZ):
		self._minZ = minZ
		
	def getMaxX(self):
		return self._maxX
		
	def setMaxX(self, maxX):
		self._maxX = maxX
		
	def getMaxY(self):
		return self._maxY
		
	def setMaxY(self, maxY):
		self._maxY = maxY

	def getMaxZ(self):
		return self._maxZ
		
	def setMaxZ(self, maxZ):
		self._maxZ = maxZ
		
	def getMidX(self):
		return self._midX
		
	def setMidX(self, midX):
		self._midX = midX
		
	def getMidY(self):
		return self._midY
		
	def setMidY(self, midY):
		self._midY = midY

	def getMidZ(self):
		return self._midZ
		
	def setMidZ(self, midZ):
		self._midZ = midZ
		
	def getChild(self, i):
		#Returns the ith (in in 0-7) child bounds.  The order is can be viewed as binary search on z,y,x
		if i/4 < 1:
			newMinZ = minZ
			newMaxZ = midZ
		else
			newMinZ = midZ
			newMaxZ = maxZ
			
		if i%4 < 2:
			newMinY = minY
			newMaxY = midY
		else
			newMinY = midY
			newMaxY = maxY
			
		if i%2 == 0:
			newMinX = minX
			newMaxX = midX
		else
			newMinX = midX
			newMaxX = maxX
			
		return Bounds(minX, minY, minZ, maxX, maxY, maxZ)
		

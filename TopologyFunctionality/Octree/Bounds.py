class Bounds(object):

	def __init__(self, minX, minY, minZ, maxX, maxY, maxZ):
		self.minX = minX
		self.minY = minY
		self.minZ = minZ
		self.maxX = maxX
		self.maxY = maxY
		self.maxZ = maxZ
		self.midX = (maxX - minX)/2
		self.midY = (maxY - minY)/2
		self.midZ = (maxZ - minZ)/2
		
	def containsPoints(self, points):
		contains = []
		for point in points:
			if  >=point.X 
		return contains		
		
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
		

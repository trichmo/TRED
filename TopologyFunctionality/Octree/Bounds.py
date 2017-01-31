class Bounds(object):

	def __init__(self, minX, minY, minZ, maxX, maxY, maxZ):
		self.minX = minX
		self.minY = minY
		self.minZ = minZ
		self.maxX = maxX
		self.maxY = maxY
		self.maxZ = maxZ
		self.midX = (maxX + minX)/2
		self.midY = (maxY + minY)/2
		self.midZ = (maxZ + minZ)/2
		
	def containsPoints(self, points):
		contains = []
		i=0
		for point in points:
			if self.minX < point.X <= self.maxY and self.minY < point.Y <= self.maxY and self.minY < point.Y <= self.maxY:
				contains.append(i)
			i=i+1
		return contains		
		
	def getChild(self, i):
		#Returns the ith (in in 0-7) child bounds.  The order can be viewed as binary search on z,y,x
		if i/4 < 1:
			newMinZ = self.minZ
			newMaxZ = self.midZ
		else:
			newMinZ = self.midZ
			newMaxZ = self.maxZ
			
		if i%4 < 2:
			newMinY = self.minY
			newMaxY = self.midY
		else:
			newMinY = self.midY
			newMaxY = self.maxY
			
		if i%2 == 0:
			newMinX = self.minX
			newMaxX = self.midX
		else:
			newMinX = self.midX
			newMaxX = self.maxX
			
		return Bounds(newMinX, newMinY, newMinZ, newMaxX, newMaxY, newMaxZ)

                        
                        

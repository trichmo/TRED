class Point(object):

	X = property(getX, setX)
	Y = property(getY, setY)
	Z = property(getZ, setZ)
	binPath = property(getBinPath, setBinPath)

	def __init__(self, X, Y, Z, binPath):
		self._X = X
		self._Y = Y
		self._Z = Z	
		self._binPath = binPath
		
	def getX(self):
		return self._X
		
	def setX(self, X):
		self._X = X
		
	def getY(self):
		return self._Y
		
	def setMinY(self, Y):
		self._Y = Y

	def getZ(self):
		return self._Z
		
	def setZ(self, Z):
		self._Z = Z
		
	def getBinPath(self):
		return self._binPath
		
	def setBinPath(self, binPath):
		self._binPath = binPath
		
	def addToBinPath(self, bins):
		self._binPath.extend(bins)
		
	def shortenBinPath(self, num):
		del self._binPath[-num:]
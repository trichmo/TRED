class Point(object):

	binPath = property(getBinPath, setBinPath)

	def __init__(self, X, Y, Z, binPath):
		self._X = X
		self._Y = Y
		self._Z = Z	
		self._binPath = binPath
		
		
	def addToBinPath(self, bins):
		self._binPath.extend(bins)
		
	def shortenBinPath(self, num):
		del self._binPath[-num:]

from TopologyFunctionality.Octree.Point import Point

def getPointObjects(x,y):
	pointObjs = []
	for idx in range(x.size):
		a=x[idx]
		b=y[idx]
		newObj = Point(a,b,0)
		pointObjs.append(newObj)
	return pointObjs
	

from TopologyFunctionality.Helper import OctreeUtil as ou
from TopologyFunctionality.Octree import Octree as oct

def getKdSubsampling(bounds,points):
    pointObjs = []
    for point in points:
        pointObjs.append( ou.getPointObjects(point[0],point[1]))
    myOctree = oct.Octree(5)
    myOctree.createOctree(pointObjs, True)
    return myOctree.getKdSubsamplePoints()

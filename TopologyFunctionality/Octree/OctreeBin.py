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
            pts=[]
            newChild = OctreeBin(self,pts,childBound, self.depth+1)
            self.children.append(newChild)
        for point in self.points:
            idx = self.findIndex(point)
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

    def removePoint(self,point):
        self.points.remove(point)

    def findIndex(self,point):
        idx=0
        if(point.Z > self.bounds.midZ):
            idx=4
        if(point.Y > self.bounds.midY):
            idx = idx + 2
        if(point.X > self.bounds.midX):
            idx = idx + 1
        return idx

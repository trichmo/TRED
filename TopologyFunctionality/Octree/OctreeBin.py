from .Bounds import Bounds

class OctreeBin(object):

    #Children always stored so binary search works as:
    #is greater than zMid, is greater than yMid, is greather than xMid
    #if true, lies to right else to left, greater for all at index 7. Less for all at index 0

    def __init__(self, parent, points, bounds,depth, trajCt):
        self.children = []
        self.points = points
        self.parent = parent
        self.bounds = bounds
        self.depth = depth
        self.trajCt = trajCt
                
    def divide(self):
        for i in range(8):
            childBound = self.bounds.getChild(i)
            pts=[]
            newChild = OctreeBin(self,pts,childBound, self.depth+1,0)
            self.children.append(newChild)
        for point in self.points:
            idx = self.findIndex(point)
            self.children[idx].addPoints([point])
            point.addToBinPath([idx])
        self.points=[]

    #Curretly Not Implemented with Trajectories
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

    def dimensionsShared(self,compBin):
        #Important to note that the bins of adjacent points must be adjacent
        if self.bounds.midX == compBin.bounds.midX:
            xPlane = None
        elif self.depth == compBin.depth:
            if self.bounds.midX > compBin.bounds.midX:
                xPlane = self.bounds.minX
            else:
                xPlane = compBin.bounds.minX
        else:
            if self.bounds.midX > compBin.bounds.midX:
                if self.bounds.minX == compBin.bounds.minX:
                    xPlane = compBin.bounds.maxX
                else:
                    xPlane = self.bounds.minX
            else:
                if compBin.bounds.minX == self.bounds.minX:
                    xPlane = self.bounds.maxX
                else:
                    xPlane = compBin.bounds.minX
            
        if self.bounds.midY == compBin.bounds.midY:
            yPlane = None
        elif self.depth == compBin.depth:
            if self.bounds.midY > compBin.bounds.midY:
                yPlane = self.bounds.minY
            else:
                yPlane = compBin.bounds.minY
        else:
            if self.bounds.midY > compBin.bounds.midY:
                if self.bounds.minY == compBin.bounds.minY:
                    yPlane = compBin.bounds.maxY
                else:
                    yPlane = self.bounds.minY
            else:
                if compBin.bounds.minY == self.bounds.minY:
                    yPlane = self.bounds.maxY
                else:
                    yPlane = compBin.bounds.minY

        if self.bounds.midZ == compBin.bounds.midZ:
            zPlane = None
        elif self.depth == compBin.depth:
            if self.bounds.midZ > compBin.bounds.midZ:
                zPlane = self.bounds.minZ
            else:
                zPlane = compBin.bounds.minZ
        else:
            if self.bounds.midZ > compBin.bounds.midZ:
                if self.bounds.minZ == compBin.bounds.minZ:
                    zPlane = compBin.bounds.maxZ
                else:
                    zPlane = self.bounds.minZ
            else:
                if compBin.bounds.minZ == self.bounds.minZ:
                    zPlane = self.bounds.maxZ
                else:
                    zPlane = compBin.bounds.minZ
        return xPlane, yPlane, zPlane

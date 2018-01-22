from TopologyFunctionality.Helper import OctreeUtil as ou

class TrajectorySegment(object):

    def __init__(self,point1,point2,tempPoints):
        self.front = point1
        self.back = point2
        self.front.addTrajectory(self)
        self.back.addTrajectory(self)
        self.tempPoints = []
        self.tempPoints = tempPoints
        if tempPoints is not None:
            for tempPoint in self.tempPoints:
                tempPoint.addTrajectory(self)

    def killTrajectory(self, anyBin):
        ou.removeTraj(self.front,self.back)
        self.front.removeTrajectory(self)
        self.back.removeTrajectory(self)
        if self.tempPoints is not None:
            for tempPoint in self.tempPoints:
                closestRelative = tempPoint.findClosestRelative([self.front,self.back])
                ou.removeTempPt(tempPoint,closestRelative)
                tempPoint.removeTrajectory(self)

    def isBackPoint(self, questionPt):
        return questionPt in self.tempPoints or questionPt == self.back

        
    def contains(self,point):
        if point == self.front or point == self.back:
            return True
        return False

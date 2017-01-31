class TrajectorySegment(object):

    def __init__(self,point1,point2,tempPoints):
        self.front = point1
        self.back = point2
        self.front.addTrajectory(self)
        self.back.addTrajectory(self)
        self.tempPoints = tempPoints
        if tempPoints is not None:
            for tempPoint in self.tempPoints:
                tempPoint.addTrajectory(self)

    def killTrajectory(self,octree):
        self.front.removeTrajectory(self)
        self.back.removeTrajectory(self)
        if self.tempPoints is not None:
            for tempPoint in self.tempPoints:
                newBin = octree.getBin(tempPoint.binPath)
                newBin.trajCt = newBin.trajCt-1
                newBin.removePoint(tempPoint)
                tempPoint.removeTrajectory(self)

    def isBackPoint(self, questionPt):
        return questionPt in self.tempPoints or questionPt == self.back

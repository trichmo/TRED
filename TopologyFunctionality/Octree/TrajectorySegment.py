from TopologyFunctionality.Helper import OctreeUtil as ou

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

    def killTrajectory(self, anyBin):
        firstBin = ou.getFirstLevelBin(anyBin)
        ou.removeTrajFromBinPath(firstBin,self.front,self.back)
        self.front.removeTrajectory(self)
        self.back.removeTrajectory(self)
        backBin = ou.getBin(firstBin,self.back.binPath)
        if self.tempPoints is not None:
            for tempPoint in self.tempPoints:
                newBin = ou.getTempPtBin(firstBin,tempPoint.binPath,tempPoint)
                closestRelative = tempPoint.findClosestRelative([self.front,self.back])
                tempPoint.binPath = ou.updateTempPointBinPath(tempPoint,firstBin)
                ou.removeTrajFromBinPath(firstBin,closestRelative,tempPoint)
                #newBin.removePoint(tempPoint)
                tempPoint.removeTrajectory(self)

    def isBackPoint(self, questionPt):
        return questionPt in self.tempPoints or questionPt == self.back

        
    def contains(self,point):
        if point == self.front or point == self.back:
            return True
        return False

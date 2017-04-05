import pdb
class Point(object):

        pointId = 0

        def __init__(self, X, Y, Z):
                self.X = X
                self.Y = Y
                self.Z = Z      
                self.binPath=[]
                self.trajectories = []
                self.pointId = Point.pointId
                Point.pointId += 1 

        def __lt__(self,other):
                return self.pointId<other.pointId
        def __gt__(self,other):
                return self.pointId>other.pointId
        def __eq__(self,other):
                return self.pointId==other.pointId
        def __le__(self,other):
                return self.pointId<=other.pointId
        def __ge__(self,other):
                return self.pointId>=other.pointId
        def __ne__(self,other):
                return self.pointId!=other.pointId

        def __repr__(self):
                return "%f %f %f" % (self.X,self.Y,self.Z)
                
        def addToBinPath(self, bins):
                self.binPath.extend(bins)
                
        def shortenBinPath(self, num):
                del self.binPath[-num:]

        def startNewTrajectory():
                Point.pointId += 2

        def addTrajectory(self, newTrajectory):
                self.trajectories.append(newTrajectory)

        def removeTrajectory(self, oldTrajectory):
                self.trajectories.remove(oldTrajectory)

        def getTrajectoryAsEnd(self):
                for traj in self.trajectories:
                        if traj.back==self:
                                return traj
                return None

        def findClosestRelative(self, points):
                closestRelative = points[0]
                closestCount=0
                myLen = len(self.binPath)
                for point in points:
                        currCount=0
                        minLen = min(myLen,len(point.binPath))
                        i=0
                        while self.binPath[i] == point.binPath[i]:
                                currCount = currCount+1
                                i=i+1
                                if i==minLen:
                                        break
                        if currCount>closestCount:
                                closestCount = currCount
                                closestRelative = point
                return closestRelative
                        

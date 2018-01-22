import pdb
class Point(object):

        pointId = 0

        def __init__(self, X, Y, Z, prevPt = None, nextPt = None):
                self.X = X
                self.Y = Y
                self.Z = Z      
                self.lowestBin=None
                self.trajectories = []
                self.nxt = nextPt
                self.prev = prevPt

        def __repr__(self):
                return "%f %f %f" % (self.X,self.Y,self.Z)
            
        def setPrev(self,pt):
            self.prev = pt
            
        def setNext(self,pt):
            self.nxt = pt
                
        def updateBin(self, bin):
            self.lowestBin = bin
        
        def updateBinToParent(self):
            self.lowestBin = self.lowestBin.parent

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
                for point in points:
                    lowestBin = self.getLowestBinMatch(point)
                    depth = lowestBin.depth
                    if depth>closestCount:
                        closestCount = depth
                        closestRelative = point
                return closestRelative
                        
        def getLowestBinMatch(self,point):
            myBin = self.lowestBin
            yourBin = point.lowestBin
            myBin,yourBin = myBin.matchBinDepths(yourBin)
            while myBin != yourBin:
                myBin = myBin.parent
                yourBin = yourBin.parent
            return myBin
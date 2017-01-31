class Point(object):

        def __init__(self, X, Y, Z):
                self.X = X
                self.Y = Y
                self.Z = Z      
                self.binPath=[]
                self.trajectories = []
                
                
        def addToBinPath(self, bins):
                self.binPath.extend(bins)
                
        def shortenBinPath(self, num):
                del self.binPath[-num:]

        def addTrajectory(self, newTrajectory):
                self.trajectories.append(newTrajectory)

        def removeTrajectory(self, oldTrajectory):
                self.trajectories.remove(oldTrajectory)

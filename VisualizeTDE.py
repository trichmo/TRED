import matplotlib.pyplot as plt
from TopologyFunctionality.Startup import Startup
from TopologyFunctionality.Helper import TimeDelayEmbeddingUtil as tde
from TopologyFunctionality.Helper import OctreeUtil as ou
from TopologyFunctionality.Octree import Octree
import Subsampling as ss
import numpy as np
import math
import matplotlib.patches as patches
import time
import csv
import os
import msvcrt as m
import pdb

class Image(object):
    
    def __init__(self,fig,ax,subjectId):
        self.fig = fig
        self.ax = ax
        #self.wave = np.array(Startup())
        testortrain = ['train', 'test']
        iterations = ['1','2','3','4']
        #subjectId = '380'
        for tot in testortrain:
            for iteration in iterations:
                saveLocation = '.\\Data\\Subject' + subjectId + '\\Subsamples_' + tot + '\\It_' +iteration + '\\'
                self.windows = ss.getWindowedPoints(subjectId,iteration,tot)
                i=0
                totTime=0
                for window in self.windows:
                    self.wave = window
                    self.waveLength = len(self.wave)

                    self.waveStart = 0
                    self.waveEnd = tde.getWaveEnd(self.waveStart)

                    self.x = [float(i[0]) for i in self.wave]
                    self.y = [float(i[1]) for i in self.wave]
                    self.z = [float(i[2]) for i in self.wave]
        ##            self.x = ss.getBaseWindow(self.allx,-2)
        ##            self.x.extend(ss.getBaseWindow(self.allx,-1))
        ##            self.y = ss.getBaseWindow(self.ally,-2)
        ##            self.y.extend(ss.getBaseWindow(self.ally,-1))
                    self.x = np.array(self.x)
                    self.y = np.array(self.y)
                    self.z = np.array(self.z)
        ##            self.iterationx = 0
        ##            self.iterationy = 0
        ##            self.sampleNo = 0
        ##            
        ##
        ##            self.oldX = []
        ##            self.oldY = []
        ##            self.newX = []
        ##            self.newY = []
                    self.points = ou.getPointObjects(self.x,self.y,self.z)
                    binThreshold = math.ceil(1000/len(self.points))
                    binThreshold = min(3,binThreshold)
                    start = time.perf_counter()
                    self.oct = Octree.Octree(4,binThreshold)
                    self.oct.createOctree(self.points,False)
                    #self.drawScatter()
                    #self.drawOctree()
                    #self.ax.set(adjustable='box-forced', aspect='equal')
                    #self.ax.set_ylim(-1.5,1.5)
                    #self.ax.set_xlim(-1.5,1.5)
                    #np.vectorize(lambda ax:ax.axis('off'))(ax)
                    #self.fig.canvas.draw()
                    totTime = totTime + (time.perf_counter() - start)
                    #print(i)
                    sample = self.oct.getKdSubsamplePoints()
                    while len(sample) < 3 and self.oct.trajThresh > 1:
                        self.oct.decreaseThreshold();
                        sample = self.oct.getKdSubsamplePoints()
                    if not os.path.exists(saveLocation):
                        os.makedirs(saveLocation)
                    with open(saveLocation + 'joint'+str((i%4)+1)+'window'+str((i//4)+1)+'.csv', 'w', newline='') as outFile:
                        writer = csv.writer(outFile)
                        for point in sample:
                            writer.writerow(point)
                    i=i+1
                    #m.getch()
        print(totTime/i)
        
        
    def drawScatter(self):
        orig = self.ax.scatter(self.x,self.y,color='k')
        #plt.setp(orig,linewidth=1)
        #old = self.ax.scatter(self.oldX,self.oldY,color='r')
        #plt.setp(old,linewidth=1)
        #new = self.ax.scatter(self.newX,self.newY,color='c')
        #plt.setp(new,linewidth=1)
        tempX=[]
        tempY=[]

    def drawPlot(self, event):
        if event.key not in ('n', 'p','k'):
            return
        if event.key == 'n':
            self.oldX = self.x[:100]
            self.oldY = self.y[:100]
            self.newX = np.array(ss.getWindow(self.allx,self.iterationx))
            self.newY = np.array(ss.getWindow(self.ally,self.iterationy))
            self.x = np.concatenate((self.x[100:],self.newX))
            self.y = np.concatenate((self.y[100:],self.newY))
            self.iterationx += 1
            self.iterationy += 1
            newPoints = ou.getPointObjects(self.newX,self.newY)
            self.oct.appendPoints(newPoints)
            #self.slideWindow(15)
            self.points, isEqual = self.test(self.oct,self.points,newPoints)
        #elif event.key == 'p':
        #    a=1
            #self.slideWindow(-15)
        elif event.key == 'k':
            sample = self.oct.getKdSubsamplePoints()
            self.sampleNo+=1
            with open('sampling'+str(self.sampleNo)+'.csv', 'w', newline='') as outFile:
                writer = csv.writer(outFile)
                for point in sample:
                    writer.writerow(point)
        plt.cla()
        plt.axis('equal')
        self.ax.set_ylim(-1.5,1.5)
        self.ax.set_xlim(-1.5,1.5)
        self.drawScatter()
        self.drawOctree()
        np.vectorize(lambda ax:ax.axis('off'))(ax)
        self.fig.canvas.draw()

    def slideWindow(self, distance):
        if self.waveStart+distance<0 or self.waveEnd+distance>self.waveLength or distance==0:
            return
        else:
            self.waveStart = self.waveStart+distance
            if distance>0:
                self.oldX=self.x[:distance]
                self.oldY=self.y[:distance]
                (self.newX,self.newY) = tde.slidePhaseSpace(self.wave,self.waveEnd+44,distance,self.tauX)
                self.x=np.concatenate((self.x[distance:],self.newX))
                self.y=np.concatenate((self.y[distance:],self.newY))
                newPts = ou.getPointObjects(self.newX,self.newY)
                self.oct.appendPoints(newPts)
            else:
                self.oldX=self.x[distance:]
                self.oldY=self.y[distance:]
                (self.newX,self.newY) = tde.slidePhaseSpace(self.wave,self.waveStart,distance,self.tauX)
                self.x=np.concatenate((self.newX,self.x[:distance]))
                self.y=np.concatenate((self.newY,self.y[:distance]))
                newPts = ou.getPointObjects(self.newX,self.newY)
                self.oct.prependPoints(newPts)
            self.waveEnd = self.waveEnd+distance
            
            
    def drawOctree(self):
        binFacts = self.oct.drawBins(self.oct.firstLevel)
        for bounds, intensity, isKey in binFacts:
            #if intensity!=0:
            if intensity>1:
                intensity=1
            elif intensity == 0:
                self.ax.add_patch(patches.Rectangle((bounds.minX,bounds.minY),bounds.maxX-bounds.minX,bounds.maxY-bounds.minY,alpha=(intensity+0.1),color='w',ec='k'))
            if isKey:
                self.ax.add_patch(patches.Rectangle((bounds.minX,bounds.minY),bounds.maxX-bounds.minX,bounds.maxY-bounds.minY,alpha=intensity,color='c',ec='k'))
            else:
                self.ax.add_patch(patches.Rectangle((bounds.minX,bounds.minY),bounds.maxX-bounds.minX,bounds.maxY-bounds.minY,alpha=intensity,color='b',ec='k'))
            

    def test(self,octDyn,pts,newPts):
        #pts[len(newPts):].extend(newPts)
        #staticPts = ou.copyPointObjects(pts)
        #octStatic = Octree.Octree(5,octDyn.bounds)
        #octStatic.createOctree(staticPts,True)
        
##        myfig, myax = plt.subplots(1,1)
##        plt.cla()
##        plt.axis('equal')
##        myax.set_ylim(-1.5,1.5)
##        myax.set_xlim(-1.5,1.5)
##        myax.scatter([point.X for point in octDyn.points],[point.Y for point in octDyn.points],color='k')
##        plt.show()
        
        #isEqual = octDyn.compare(octStatic)
        #print(isEqual)
        isEqual = True
        return pts, isEqual
    
if __name__ == '__main__':
    fig, ax = plt.subplots(1,1)
    subjects = ['015','059','274','292','380','390','454','503','805','875','909']
    for subject in subjects:
        image = Image(fig,ax,subject)
    #fig.canvas.mpl_connect('key_press_event',image.drawPlot)
    #plt.show()

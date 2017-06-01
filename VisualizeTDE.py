import matplotlib.pyplot as plt
from TopologyFunctionality.Startup import Startup
from TopologyFunctionality.Helper import TimeDelayEmbeddingUtil as tde
from TopologyFunctionality.Helper import OctreeUtil as ou
from TopologyFunctionality.Octree import Octree
from TopologyFunctionality.Octree import Bounds
from TopologyFunctionality.Octree import Point
import math
import Subsampling as ss
import numpy as np
import matplotlib.patches as patches
import time
import csv

class Image(object):
    
    def __init__(self,fig,ax,use):
        self.fig = fig
        self.ax = ax
        self.points=[]
        self.x = []
        self.y = []
        if use == 'map':
            initMapping()
        elif use == 'activity':
            initActivityRecognition()
        else:
            print('Please enter expected use')
            return
        self.drawScatter()
        self.drawOctree()
        self.ax.set(adjustable='box-forced', aspect='equal')
        np.vectorize(lambda ax:ax.axis('off'))(ax)
        self.fig.canvas.draw()
        
        
        
        #self.wave = np.array(Startup())

        self.wave = ss.getMapPoints()
        self.waveLength = len(self.wave)

        self.waveStart = 0
        self.waveEnd = tde.getWaveEnd(self.waveStart)
        #self.waveLength = self.wave.size
        #[self.x,self.y, self.tauX] = tde.getPhaseData(self.wave, self.waveStart, self.waveEnd)

        self.points=[]
        self.x = []
        self.y = []
        self.maxX = float("-inf")
        self.maxY = float("-inf")
        self.minX = float("inf")
        self.minY = float("inf")
        prevPt = None
        
        for idx in self.wave:
            x = float(idx[0])
            if x == -1:
                prevPt = None
            else:
                y = float(idx[1])
                if y>self.maxY:
                    self.maxY=y
                if y<self.minY:
                    self.minY=y
                if x>self.maxX:
                    self.maxX=x
                if x<self.minX:
                    self.minX=x
                newPt = ou.getPointObject(x,y,prevPt)
                if prevPt!=None:
                    prevPt.setNext(newPt)
                self.points.append(newPt)
                self.x.append(x)
                self.y.append(y)
                prevPt = newPt
                
##        self.x = ss.getBaseWindow(self.allx,-2)
##        self.x.extend(ss.getBaseWindow(self.allx,-1))
##        self.y = ss.getBaseWindow(self.ally,-2)
##        self.y.extend(ss.getBaseWindow(self.ally,-1))
##        self.x = np.array(self.x)
##        self.y = np.array(self.y)
##        self.iterationx = 0
##        self.iterationy = 0
##        self.sampleNo = 0
##        
##
##        self.oldX = []
##        self.oldY = []
##        self.newX = []
##        self.newY = []
##        self.points = ou.getPointObjects(self.x,self.y)
        self.oct = Octree.Octree(8, Bounds.Bounds(self.minX,self.minY,-1,self.maxX,self.maxY,1), 35, 100)
        start = time.perf_counter()
        self.oct.createOctree(self.points,True)
        self.drawScatter()
        self.drawOctree()
        self.ax.set(adjustable='box-forced', aspect='equal')
        np.vectorize(lambda ax:ax.axis('off'))(ax)
        self.fig.canvas.draw()
        print(time.perf_counter()-start)
        
    def initMapping():
        self.wave = ss.getMapPoints()
        self.waveLength = len(self.wave)

        self.waveStart = 0
        self.waveEnd = tde.getWaveEnd(self.waveStart)

        (tmpX, tmpY) = zip(*[(point[0],point[1]) for point in self.wave])
        bounds = getBoundsCreatePoints(tmpX,tmpY)
        #insert equation for determining depth from half side and noise level here
        #what should we do about determining the key bin threshold (expected number of paths?)
        self.oct = Octree.Octree(8, bounds, 35, 100)
        start = time.perf_counter()
        self.oct.createOctree(self.points,True)
        print(time.perf_counter()-start)

        
    def initActivityRecognition():
        self.wave = ss.getPointsFromFile()
        self.waveLength = len(self.wave)
        self.waveStart = 0
        self.waveEnd = tde.getWaveEnd(self.waveStart)
        [tempx,tempy,self.tauX] = tde.getPhaseData(self.wave,self.waveStart,self.waveEnd)
        bounds = getBoundsCreatePoints(tempx,tempy)
        self.oct = Octree.Octree(5,bounds,5,10)
        start = time.perf_counter()
        self.oct.createOctree(self.points,True)
        print(time.perf_counter()-start)
        
    def getBoundsCreatePoints(self,x,y):
        self.maxX = float("-inf")
        self.maxY = float("-inf")
        self.minX = float("inf")
        self.minY = float("inf")
        prevPt = None
        for idx in x:
            x = float(x[0])
            if math.isnan(x):
                prevPt = None
            else:
                y = float(idx[1])
                if y>self.maxY:
                    self.maxY=y
                if y<self.minY:
                    self.minY=y
                if x>self.maxX:
                    self.maxX=x
                if x<self.minX:
                    self.minX=x
                newPt = ou.getPointObject(x,y,prevPt)
                if prevPt!=None:
                    prevPt.setNext(newPt)
                self.points.append(newPt)
                self.x.append(x)
                self.y.append(y)
                prevPt = newPt
        midX = (self.maxX + self.minX)/2
        midY = (self.maxY + self.minY)/2
        halfSide = max(maxX-midX,maxY-midY)
        return Bounds.Bounds(self.midX-halfSide,self.midY-halfSide,-1,self.midX+halfSide,self.midY+halfSide,1)
        
    def drawScatter(self):
        orig = self.ax.scatter(self.x,self.y,color='k',s=1)
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
            """self.oldX = self.x[:100]
            self.oldY = self.y[:100]
            self.newX = np.array(ss.getWindow(self.allx,self.iterationx))
            self.newY = np.array(ss.getWindow(self.ally,self.iterationy))
            self.x = np.concatenate((self.x[100:],self.newX))
            self.y = np.concatenate((self.y[100:],self.newY))
            self.iterationx += 1
            self.iterationy += 1
            newPoints = ou.getPointObjects(self.newX,self.newY)
            self.oct.appendPoints(newPoints)"""
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
        #self.drawScatter()
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
        binFacts, checkExtendedFamily = self.oct.getDualScaleBins(self.oct.firstLevel)
        shiftFacts = ou.getExtendedFamilyShifts(checkExtendedFamily)
        if shiftFacts is not None:
            binFacts.extend(shiftFacts)
        #binFacts = self.oct.drawBins(self.oct.firstLevel)
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
        pts[len(newPts):].extend(newPts)
        staticPts = ou.copyPointObjects(pts)
        octStatic = Octree.Octree(8, octDyn.bounds, 35, 100)
        octStatic.createOctree(staticPts,True)
        
##        myfig, myax = plt.subplots(1,1)
##        plt.cla()
##        plt.axis('equal')
##        myax.set_ylim(-1.5,1.5)
##        myax.set_xlim(-1.5,1.5)
##        myax.scatter([point.X for point in octDyn.points],[point.Y for point in octDyn.points],color='k')
##        plt.show()
        
        isEqual = octDyn.compare(octStatic)
        print(isEqual)
        isEqual = True
        return pts, isEqual
    
if __name__ == '__main__':
    fig, ax = plt.subplots(1,1)
    image = Image(fig,ax)
    fig.canvas.mpl_connect('key_press_event',image.drawPlot)
    plt.show()

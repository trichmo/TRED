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
import matplotlib.transforms as transforms
import time
import csv
import os
import msvcrt as m
import pdb
from scipy import ndimage
from skimage import morphology
from skimage import io
import bisect
import PIL

class Image(object):
    
    def __init__(self,fig,ax,use,sub_idx=None):
        self.fig = fig
        self.ax = ax
        self.points=[]
        self.x = []
        self.y = []
        if use == 'map':
            self.initMapping()
        elif use == 'activity':
            self.initActivityRecognition(sub_idx)
            print(self.runtime/self.tot_run)
        elif use == 'misc':
            self.initMisc()
        else:
            print('Please enter expected use')
            print('Unknown Use: ')
            print(use)
            return
        self.saveKDE('C:\\Users\\trichmo\\Projects\\PythonTopology\\Data\\map\\kde_imgs\\')
        #self.visualizePaths()
        #self.drawOctree()      
        #plt.show()
    
        
    def initMapping(self):
        self.wave = ss.getMapPoints()
        self.waveLength = len(self.wave)

        self.waveStart = 0
        self.waveEnd = tde.getWaveEnd(self.waveStart)

        (tmpX, tmpY) = zip(*[(point[0],point[1]) for point in self.wave])
        bounds = self.getBoundsCreatePoints(tmpX,tmpY)
        #self.visualizePaths()
        #plt.show()
        #return
        binDepth = 11
        self.preprocessData(bounds,binDepth)
        self.ax.set_xlim([bounds.minX, bounds.maxX])
        self.ax.set_ylim([bounds.minY, bounds.maxY])
        self.oct = Octree.Octree(binDepth, bounds, 10, 100)
        start_time = time.time()
        self.oct.createOctree(self.points,True)
        print("runtime : {}".format(time.time() - start_time))
        
        
    def initRoach(self):
        self.wave = ss.getRoachPoints()
        self.waveLength = len(self.wave)

        self.waveStart = 0
        self.waveEnd = tde.getWaveEnd(self.waveStart)

        (tmpX, tmpY) = zip(*[(point[1],point[2]) for point in self.wave])
        bounds = self.getBoundsCreatePoints(tmpX,tmpY)
        binDepth = 6
        self.oct = Octree.Octree(binDepth, bounds, 4, 4)
        self.oct.createOctree(self.points,True)
        
    def initMisc(self):
        self.wave = ss.getPointsFromFile()
        self.waveStart = 0
        self.waveEnd = tde.getWaveEnd(self.waveStart)
        self.x = [float(i[0]) for i in self.wave]
        self.y = [float(i[1]) for i in self.wave]
        self.z = [float(i[2]) for i in self.wave]
        self.x = np.array(self.x)
        self.y = np.array(self.y)
        self.z = np.array(self.z)
        self.points = ou.getPointObjects(self.x,self.y,self.z)
        binThreshold = 2
        bounds = self.getBoundsThree(self.points)
        self.oct = Octree.Octree(4,bounds,binThreshold,10)
        start = time.perf_counter()
        self.oct.createOctree(self.points,True)
        self.visualizePaths()
        self.drawOctree()
        plt.show()
        sample = self.oct.getKdSubsamplePoints()
        print(time.perf_counter()-start)
        
        
    def visualizePaths(self):
        currIdx = - 1
        num_pts = len(self.points) - 1
        while currIdx < num_pts:
            x = []
            y = []
            z = []
            currIdx += 1
            currPt = self.points[currIdx]
            while currPt.nxt:
                x.append(currPt.X)
                y.append(currPt.Y)
                z.append(currPt.Z)
                currPt = currPt.nxt
                currIdx += 1
            self.ax.plot(x,y,c='k',lw=0.3,alpha=0.7)
    
    def preprocessData(self, bounds, binDepth):
        min_dist = max((bounds.maxX - bounds.minX),(bounds.maxY - bounds.minY))/(2**binDepth)
        new_points=[]
        for idx, pt in enumerate(self.points):
            prevPt = pt.prev
            if prevPt != None:
                max_coord_dist = max(abs(pt.X - prevPt.X),abs(pt.Y - prevPt.Y))
                if  max_coord_dist > min_dist:
                    num_points = math.ceil(max_coord_dist/min_dist)
                    dist_added_x = (pt.X - prevPt.X)/num_points
                    dist_added_y = (pt.Y - prevPt.Y)/num_points
                    dist_added_z = (pt.Z - prevPt.Z)/num_points
                    add_pts = []
                    for sub_idx in range(num_points):
                        xval = prevPt.X + dist_added_x*(sub_idx+1)
                        yval = prevPt.Y + dist_added_y*(sub_idx+1)
                        zval = prevPt.Z + dist_added_z*(sub_idx+1)
                        add_pts.append((xval,yval,zval,idx))
                    new_points.append(add_pts)
        for point_list in new_points:
            first_pt = point_list[0]
            append_prev = self.points[first_pt[3]]
            append_last = append_prev.nxt
            for point in point_list:
                new_pt = ou.getPointObject(point[0],point[1],point[2],prevPt = append_prev)
                append_prev.setNext(new_pt)
                append_prev = new_pt
                self.points.append(new_pt)
            append_prev.setNext(append_last)
            if append_last:
                append_last.setPrev(append_prev)
        
    def initActivityRecognition(self,sub_idx):
        #testortrain = ['test','train']
        testortrain = ['test']
        #iterations = ['1','2','3','4']
        iterations = ['1']
        self.runtime = 0
        self.tot_run = 0
        for tot in testortrain:
            for iteration in iterations:
                saveLocation = '.\\Data\\Subject' + sub_idx + '\\Subsamples_'+tot+'\\It_'+iteration+'\\'
                self.windows = ss.getWindowedPoints(sub_idx,iteration,tot)
                i=0
                for window in self.windows:
                    self.wave = window
                    self.waveStart = 0
                    self.waveEnd = tde.getWaveEnd(self.waveStart)
                    self.x = [float(i[0]) for i in self.wave]
                    self.y = [float(i[1]) for i in self.wave]
                    self.z = [float(i[2]) for i in self.wave]
                    self.x = np.array(self.x)
                    self.y = np.array(self.y)
                    self.z = np.array(self.z)
                    self.points = ou.getPointObjects(self.x,self.y,self.z)
                    binThreshold = math.ceil(1000/len(self.points))
                    binThreshold = min(3,binThreshold)
                    bounds = self.getBoundsThree(self.points)
                    self.oct = Octree.Octree(4,bounds,binThreshold,10)
                    start = time.perf_counter()
                    self.oct.createOctree(self.points,True)
                    self.runtime += time.perf_counter()-start
                    self.tot_run += 1
                    # sample = self.oct.getKdSubsamplePoints()
                    # while len(sample) < 3 and self.oct.trajThreshold > 1:
                        # self.oct.decreaseThreshold()
                        # sample = self.oct.getKdSubsamplePoints()
                    # if not os.path.exists(saveLocation):
                        # os.makedirs(saveLocation)
                    # with open(saveLocation + 'joint'+str((i%6)+1)+'window'+str((i//6)+1)+'.csv','w',newline='') as outFile:
                        # writer = csv.writer(outFile)
                        # for point in sample:
                            # writer.writerow(point)
                    # i+=1      
                    # plt.cla()
                    del self.oct                    
        
    def getBoundsThree(self,points):
        self.maxX = float("-inf")
        self.maxY = float("-inf")
        self.maxZ = float("-inf")
        self.minZ = float("inf")
        self.minX = float("inf")
        self.minY = float("inf")
        for point in points:
            if point.Y>self.maxY:
                self.maxY=point.Y
            if point.Y<self.minY:
                self.minY=point.Y
            if point.X>self.maxX:
                self.maxX=point.X
            if point.X<self.minX:
                self.minX=point.X
            if point.Z>self.maxZ:
                self.maxZ=point.Z
            if point.Z<self.minZ:
                self.minZ=point.Z
        midX = (self.maxX + self.minX)/2
        midY = (self.maxY + self.minY)/2
        midZ = (self.maxZ + self.minZ)/2
        halfSide = max(self.maxZ-midZ,self.maxY-midY,self.maxX-midX)
        return Bounds.Bounds(midX-halfSide,midY-halfSide,midZ-halfSide,midX+halfSide,midY+halfSide,midZ+halfSide)
        
    def getBoundsCreatePoints(self,xList,yList):
        self.maxX = float("-inf")
        self.maxY = float("-inf")
        self.minX = float("inf")
        self.minY = float("inf")
        prev_pt = None
        for idx, x in enumerate(xList):
            x = float(xList[idx])
            if math.isnan(x):
                prev_pt = None
            else:
                y = float(yList[idx])
                if y>self.maxY:
                    self.maxY=y
                if y<self.minY:
                    self.minY=y
                if x>self.maxX:
                    self.maxX=x
                if x<self.minX:
                    self.minX=x
                newPt = ou.getPointObject(x,y, 0,prevPt = prev_pt)
                if prev_pt!=None:
                    prev_pt.setNext(newPt)
                self.points.append(newPt)
                self.x.append(x)
                self.y.append(y)
                prev_pt = newPt
        midX = (self.maxX + self.minX)/2
        midY = (self.maxY + self.minY)/2
        halfSide = max(self.maxX-midX,self.maxY-midY) * 1.05
        return Bounds.Bounds(midX-halfSide,midY-halfSide,-1,midX+halfSide,midY+halfSide,1)
        
    def drawScatter(self):
        orig = self.ax.scatter(self.x,self.y,color='k',s=1)
        tempX=[]
        tempY=[]

    def drawPlot(self, event):
        if event.key not in ('n', 'p','k'):
            return
        if event.key == 'n':
            self.points, isEqual = self.test(self.oct,self.points,newPoints)
        elif event.key == 'k':
            sample = self.oct.getKdSubsamplePoints()
            self.sampleNo+=1
            with open('sampling'+str(self.sampleNo)+'.csv', 'w', newline='') as outFile:
                writer = csv.writer(outFile)
                for point in sample:
                    writer.writerow(point)
        plt.cla()
        plt.axis('equal')
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
        self.ax.scatter([self.minX, self.minX, self.maxX, self.maxX],[self.minY, self.maxY, self.minY, self.maxY],color='w',s=1)
        binFacts, checkExtendedFamily = self.oct.getDualScaleBins(self.oct.firstLevel)
        shiftFacts = ou.getExtendedFamilyShifts(checkExtendedFamily)
        if shiftFacts is not None:
            binFacts.extend(shiftFacts)
        for bounds, intensity, isKey in binFacts:
            if isKey:
                self.ax.add_patch(patches.Rectangle((bounds.minX,bounds.minY),bounds.maxX-bounds.minX,bounds.maxY-bounds.minY,alpha=0.7,color='c',ec='k',zorder=3))
            else:
                self.ax.add_patch(patches.Rectangle((bounds.minX,bounds.minY),bounds.maxX-bounds.minX,bounds.maxY-bounds.minY,alpha=0.1,color='w',ec='k'))
            

    def test(self,octDyn,pts,newPts):
        pts[len(newPts):].extend(newPts)
        staticPts = ou.copyPointObjects(pts)
        octStatic = Octree.Octree(8, octDyn.bounds, 35, 100)
        octStatic.createOctree(staticPts,True)
        isEqual = octDyn.compare(octStatic)
        print(isEqual)
        isEqual = True
        return pts, isEqual
        
    def saveKDE(self, save_loc):
        np_img = self.oct.createKDE()
        im = PIL.Image.fromarray(np_img, 'I')
        im.save(save_loc + 'kde.png')
        with open(save_loc + 'bbox.txt', 'w') as f:
            f.write(str(self.oct.bounds.minX) + ' ' + str(self.oct.bounds.minY) + ' ' + str(self.oct.bounds.maxX) + ' ' + str(self.oct.bounds.maxY))
        
        
def runMapping():
    print('starting')
    fig, ax = plt.subplots(1,1)
    image = Image(fig,ax,'map')
    figFile = 'ex.png'
    plt.savefig(figFile, dpi=1000,bbox_inches='tight',pad_inches=0)
    #return
    
    start_time = time.time()
    magGrey = io.imread(figFile,as_grey=True)
    bool_img = (magGrey == 0)
    zoomed=bool_img
    skel, distance = morphology.medial_axis(zoomed, return_distance=True)

    pruned_skel = morphology.remove_small_objects(skel,8,connectivity=2)
    print('pruned')
    
    dist_on_skel = distance * pruned_skel
    
    '''
    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(8, 4))
    ax3.imshow(zoomed, cmap=plt.cm.gray, interpolation='nearest')
    ax3.axis('off')
    ax4.imshow(dist_on_skel, cmap=plt.cm.spectral, interpolation='nearest')
    ax4.contour(zoomed, [0.5], colors='w')
    ax4.axis('off')
    fig2.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
    
    plt.show()
    '''
    
    lowest,leftmost,highest,rightmost = image.oct.getLowerLeftBox(np.inf,np.inf,-np.inf,-np.inf)
    minX = image.oct.bounds.minX
    minY = image.oct.bounds.minY
    col_len,row_len = np.shape(pruned_skel)
    rows,cols = np.where(pruned_skel)
    row_start = row_len - max(rows)
    col_start = min(cols)
    xSize = (rightmost-leftmost)/(max(cols) - col_start)
    ySize = (highest-lowest)/(max(rows) - min(rows))
    nodes = []
    node_idxs = []
    lowest_leftmost = [np.inf,np.inf]
    for row,col in zip(rows,cols):
        curridx = (row*row_len) + col
        yLoc = (row_len - row-row_start + 0.5)*ySize
        xLoc = (col - col_start + 0.5)*xSize
        nodes.append([curridx,xLoc,yLoc])
        if lowest_leftmost[0] > yLoc:
            lowest_leftmost[0] = yLoc
        if lowest_leftmost[1] > xLoc:
            lowest_leftmost[1] = xLoc
        node_idxs.append(curridx)
    for node in nodes:
        node[1] += leftmost - lowest_leftmost[1]
        node[2] += lowest - lowest_leftmost[0]
    edges = []
    edge_id=0
    node_idxs.sort()
    print('getting idcs')
    for idx in node_idxs:
        edge_adj = []
        adj_idxs = [idx-1,idx+1,idx-row_len,idx-row_len-1,idx-row_len+1,idx+row_len,idx+row_len-1,idx+row_len+1]
        insert_locs = [bisect.bisect(node_idxs,adj_idxs[0]),bisect.bisect(node_idxs,adj_idxs[1]),bisect.bisect(node_idxs,adj_idxs[2]),bisect.bisect(node_idxs,adj_idxs[3]),
                        bisect.bisect(node_idxs,adj_idxs[4]),bisect.bisect(node_idxs,adj_idxs[5]),bisect.bisect(node_idxs,adj_idxs[6]),bisect.bisect(node_idxs,adj_idxs[7])]
        for insert_idx,insert_loc in enumerate(insert_locs):
            if node_idxs[insert_loc-1] == adj_idxs[insert_idx]:
                edges.append((edge_id,idx,adj_idxs[insert_idx],1))
                edge_id +=1
    with open('tracebundle_vertices.txt','w', newline='') as save_file:
        save_writer = csv.writer(save_file)
        for row in nodes:
            save_writer.writerow(row)
    with open('tracebundle_edges.txt','w', newline='') as save_file:
        save_writer = csv.writer(save_file)
        for row in edges:
            save_writer.writerow(row)
            
    print(time.time() - start_time)
    

    
if __name__ == '__main__':
    #runMapping()
    fig, ax = plt.subplots(1,1)
    image = Image(fig,ax,'map')
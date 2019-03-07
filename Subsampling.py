from TopologyFunctionality.Helper import OctreeUtil as ou
from TopologyFunctionality.Octree import Octree as oct
import csv
import os
from math import floor
import pdb
import re

def getKdSubsampling(bounds,points):
    pointObjs = []
    for point in points:
        pointObjs.append( ou.getPointObjects(point[0],point[1]))
    myOctree = oct.Octree(5)
    myOctree.createOctree(pointObjs, True)
    return myOctree.getKdSubsamplePoints()

def getPointsFromFile():
    with open('topology.csv','r',newline='') as csvfile:
        reader = csv.reader(csvfile)
        dataStream = list(reader)
    return dataStream

def getWindowedPoints(subjectId,iteration,testortrain):
    dataStream = []
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    rootFile = '.\\Data\\Subject' + subjectId + '\\Windows_' + testortrain + '\\It_' +iteration
    unsortedFilenames = os.listdir(rootFile)
    filenames = sorted(unsortedFilenames,key=alphanum_key)
    #filenames = ['85joint6Window.csv']
    for filename in filenames:
        newStream=[]
        print(filename)
        with open(rootFile+'\\'+filename,'r') as f:
            reader = csv.reader(f)
            newStream.extend(list(reader))
        dataStream.append(newStream)
    return dataStream

def getMapPoints():
    dataStream = []
    for filename in os.listdir('.\\Data\\map\\data\\tracks\\tracks_athens_small\\athens_small\\trips'):
        with open('.\\Data\\map\\data\\tracks\\tracks_athens_small\\athens_small\\trips\\'+filename,'r') as f:
            reader = csv.reader(f,delimiter=' ')
            pt_list = list(reader)
            new_list = []
            last_pt=None
            for pt in pt_list:
                x = float(pt[0])
                y = float(pt[1])
                append_pts = []
                if last_pt:
                    dx = x - last_pt[0]
                    dy = y - last_pt[1]
                    for t in [1]:
                        new_x = dx*t + last_pt[0]
                        new_y = dy*t + last_pt[1]
                        append_pts.append([new_x,new_y])
                else:
                    append_pts.append([x,y])
                last_pt = [x,y]
                new_list.extend(append_pts)
            new_list.append(last_pt)
            dataStream.extend(new_list)
            dataStream.append(('nan','nan','nan'))
    return dataStream
    
def getRoachPoints():
    dataStream = []
    for filename in os.listdir('.\\Data\\roach\\'):
        with open('.\\Data\\roach\\'+filename,'r') as f:
            reader = csv.reader(f,delimiter=' ')
            dataStream.extend(list(reader))
    return dataStream

def getBaseWindow(dim, i):
    windowSize = 1000
    overlap = 500
    newPts = dim[(i*overlap)+windowSize:((i+1)*overlap)+windowSize]
    return newPts

def getWindow(dim, i):
    windowSize = 1000
    overlap = 500
    newPts = dim[(i*overlap)+windowSize:((i+1)*overlap)+windowSize]
    return newPts


if __name__ == '__main__':
    windowSize = 1000
    overlap = 500
    dataStream = getPointsFromFile()
    points = ou.getPointObsFromSingleSrc(dataStream)
    myOctree = oct.Octree(5)
    baseSet = points[0:windowSize]
    myOctree.createOctree(baseSet,True)
    iterations = floor((len(points)-len(baseSet))/(windowSize-overlap))
    sampling = []
    for i in range(iterations):
        newPts = points[(i*overlap)+windowSize:((i+1)*overlap)+windowSize]
        myOctree.appendPoints(newPts)
        sample = myOctree.getKdSubsamplePoints()
        sampling.append(sample)
    with open('sampling.csv', 'w', newline='') as outFile:
        writer = csv.writer(outFile)
        i=0
        for line in sampling:
            i=i+1
            for point in line:
                writer.writerow([i] + point)

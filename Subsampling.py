from TopologyFunctionality.Helper import OctreeUtil as ou
from TopologyFunctionality.Octree import Octree as oct
import csv
import os
from math import floor
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

def getWindowedPoints():
    dataStream = []
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    unsortedFilenames = os.listdir('.\\Windows')
    filenames = sorted(unsortedFilenames,key=alphanum_key)
    for filename in filenames:
        newStream=[]
        print(filename)
        with open('.\\Windows\\'+filename,'r') as f:
            reader = csv.reader(f)
            newStream.extend(list(reader))
        dataStream.append(newStream)
    return dataStream

def getBaseWindow(dim, i):
    windowSize = 2000
    overlap = 1000
    newPts = dim[(i*overlap)+windowSize:((i+1)*overlap)+windowSize]
    return newPts

def getWindow(dim, i):
    windowSize = 2000
    overlap = 100
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

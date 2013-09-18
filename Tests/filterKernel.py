from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def smoothFilter(values):
  temp=list()
  bandCount = len(values[0][0])
  for k in xrange(bandCount):
    bandValues=0
    for i in xrange(3):
      for j in xrange(3):
        bandValues = bandValues + values[i][j][k]
    bandValues = bandValues/9
    temp.append(bandValues)
  return temp

def main():
  # replace the filepath with appropriate file
  fileName='C:\Users\Sandeep\Desktop\Costa1.tif'
  layer = loadRasterLayer(fileName)
  layer.filterKernel(smoothFilter,"new3.jpg", Buffer.TYPE_BYTE, 3)
  # replace the filepath with appropriate file
  # careful with the \\ before n. As '\n' makes a newline
  # and gives wrong filename, we used '\\'
  layer1 = loadRasterLayer('C:\Users\Sandeep\Desktop\\new3.jpg')


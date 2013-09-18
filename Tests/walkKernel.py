
from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer

# gets the value of 8-neighbour whose values of all bands
# greater than the current pixel.
def maxNeighbour(values):
  temp=values[1][1]
  bandCount = len(values[0][0])
  for i in xrange(3):
    for j in xrange(3):
      state=0
      for k in xrange(bandCount):
        if(values[i][j][k]<temp[k]):
          state=1
      if state==0:
        temp=values[i][j]
  print temp

def main():
  # replace the filepath with appropriate file
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.walkKernel(maxNeighbour)


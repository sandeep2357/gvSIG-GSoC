
from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def AddOperation(values1, values2):
  values =values1
  bandCount = len(values1)
  for i in xrange(3):
    for j in xrange(3):
      for k in xrange(bandCount):
        values[i][j][k]= values1[i][j][k]+values2[i][j][k]
  return values

def main():
  # replace the filepaths with appropriate file
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer2 = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.operationKernel(AddOperation,layer2,"Operation_new.jpg",Buffer.TYPE_INT)
  # replace the filepath with appropriate file
  layer3 = loadRasterLayer("C:\Users\Sandeep\Desktop\Operation_new.jpg")



from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def AddOperation(values1, values2):
  values =list()
  for i in xrange(3):
    for j in xrange(3):
      values.append([values1[i][j][0]+values2[i][j][0],values1[i][j][1]+values2[i][j][1],values1[i][j][2]+values2[i][j][2]])
  return values

def main():
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer2 = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.operationKernel(AddOperation,layer2,"Operation_new.jpg",Buffer.TYPE_INT)
  layer3 = loadRasterLayer("C:\Users\Sandeep\Desktop\Operation_new.jpg")

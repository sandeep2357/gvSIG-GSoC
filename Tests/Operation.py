from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def AddOperation(values1, values2):
  values = values1 + values2
  return values

def main():
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer2 = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.operation(AddOperation,layer2,"Operation_new.jpg",Buffer.TYPE_INT)
  layer3 = loadRasterLayer("C:\Users\Sandeep\Desktop\Operation_new.jpg")

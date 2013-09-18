
from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def AddOperation(values1, values2):
  values=list()
  for i in xrange(len(values1)):
    values.append(values1[i]+values2[i])
  return values

def main():
  # replace the filepaths with appropriate file
  layer = loadRasterLayer('C:\Users\Sandeep\Desktop\Costa1.tif')
  layer2 = loadRasterLayer('C:\Users\Sandeep\Desktop\Costa1.tif')
  layer.operation(AddOperation,layer2,"Operation_new.jpg",Buffer.TYPE_BYTE)
  # replace the filepath with appropriate file
  layer3 = loadRasterLayer('C:\Users\Sandeep\Desktop\Operation_new.jpg')



from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def incrShine(values):
  return values[1][1]

def main():
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.filterKernel(incrShine,"new3.jpg", Buffer.TYPE_BYTE, 3)
  layer1 = loadRasterLayer("C:\Users\Sandeep\Desktop\\new3.jpg")

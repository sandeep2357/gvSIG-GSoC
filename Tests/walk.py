
from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def getValues(values):
  print values

def main():
  # replace the filepath with appropriate file
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.walk(getValues)


from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def incrShine(values):
  temp = list()
  for value in values:
    temp.append(value)
  return temp

def main():
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.walk(incrShine)
  #layer1 = loadRasterLayer("C:\Users\Sandeep\Desktop\\new3.jpg")

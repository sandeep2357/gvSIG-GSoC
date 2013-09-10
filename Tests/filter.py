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
  layer = loadRasterLayer("C:\Users\Sandeep\Desktop\cal_3arc.tif")
 
  
  layer2 = loadRasterLayer("C:\Users\Sandeep\Desktop\Costa1.tif")
  layer.filter(incrShine,"new3.jpg", Buffer.TYPE_BYTE, 1)
  layer2.filter(incrShine,"new4.jpg", Buffer.TYPE_BYTE, 3)
  layer3 = loadRasterLayer("C:\Users\Sandeep\Desktop\\new3.jpg")
  layer1 = loadRasterLayer("C:\Users\Sandeep\Desktop\\new4.jpg")

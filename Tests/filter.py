
from gvsig import *
from gvsig_raster import *
from geom import *
from org.gvsig.fmap.dal.coverage.dataset import Buffer


def incrShine(values):
  temp = list()
  for value in values:
    temp.append(value+10)
  return temp

def main():
  # replace the filepath with appropriate file
  fileName='C:\Users\Sandeep\Desktop\Costa1.tif'
  layer = loadRasterLayer(fileName)
  layer.filter(incrShine,"new3.tif", Buffer.TYPE_BYTE, 3)
  # replace the filepath with appropriate file
  # careful with the \\ before n. As '\n' makes a newline
  # and gives wrong filename, we used '\\'
  layer1 = loadRasterLayer('C:\Users\Sandeep\Desktop\\new3.tif')


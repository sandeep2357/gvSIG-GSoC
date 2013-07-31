from gvsig import *

#--------------------------------------------------------------
# This code will go to the module gvsig_raster.py 
# Now is here to debug more easily
# Begin module gvsig_raster

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.mapcontext import MapContextLocator
from org.gvsig.fmap.dal.coverage import RasterLocator
from org.gvsig.fmap.dal.coverage.store.parameter import NewRasterStoreParameters
from org.gvsig.fmap.dal.coverage.dataset import Buffer
from org.gvsig.fmap.dal.serverexplorer.filesystem import FilesystemServerExplorer
from org.gvsig.raster.fmap.layers import FLyrRaster
from java.lang import Byte,Short,Integer,Float,Double
from java.io import File

from  os.path  import splitext

def loadRasterLayer (rasterfile, mode = "r" ):
    """ 
    Load a raster file in a layer
    """ 
    if  not  isinstance (rasterfile,File):
        rasterfile = File(rasterfile)

    name, ext = splitext(rasterfile.getName())

    view = currentView()
  
    # Get the manager to use
    dalManager = DALLocator.getDataManager()
    mapContextManager = MapContextLocator.getMapContextManager()

    if ext.lower() == ".ecw" or ext.lower() == ".jp2" :
        # FIXME
        pass
    elif ext.lower() == ".mrsid":
        # FIXME
        pass
    else:
        # Create the parameters to open the raster store based in GDAL
        params = dalManager.createStoreParameters("Gdal Store")
        params.setFile(rasterfile)

    # Create the raster store
    dataStore = dalManager.createStore(params)

    # Create a raster layer based in this raster store
    layer = mapContextManager.createLayer(name, dataStore);

    view.addLayer(layer)
    return layer


## @cond FALSE
rasterLayerExtensions =  dict ()


class  RasterLayerExtensions(object):
    """
    This class hold aditional properties and operations need to manage the scripting raster layer
    (query, buffer values ​​....)
    """
    def  __init__(self, store=None):
        self.store = store
        self.buffer = None
        self.query = None
        self.values = None
        self.kernel = None
        self.setElem = None
        self.getElem = None

    def  prepareQuery(self):
        # # See RasterManager in javadocs for more info
        self.query = RasterLocator.getManager().createQuery();
        # # See RasterQuery in javadocs for more
        self.query.setAllDrawableBands()
        self.query.setAreaOfInterest()
        self.buffer = None
        self.values = None
        self.kernel = None

    def createBuffer(self):
        self.buffer = self.store.query(self.getQuery())

    def createNewBuffer(self,width, height, bandcount, datatype):
        if self.store != None:
            raise RuntimeException("Can't create a new buffer associated to a store")

        # FIXME: workaround to work with a jython bug passing byte, short and
        # double values as parameters
        if datatype in (Buffer.TYPE_BYTE, Buffer.TYPE_SHORT, Buffer.TYPE_INT):
            datatype = Buffer.TYPE_INT
        else:
            datatype = Buffer.TYPE_FLOAT
        # End workaround

        self.buffer = RasterLocator.getManager().createBuffer(
            int(datatype),
            int(width),
            int(height),
            int(0 if bandcount is None else bandcount),
            True
        )
        self.prepareBuffer(self.buffer)

    def prepareBuffer(self, buffer):
        def setElemByte(buffer, line, col, band, data):
            buffer.setElem(line, col, band, Byte(data).byteValue())

        def  setElemShort (buffer, line, col, band, date):
            buffer.setElem(line, col, band, Short(date).shortValue())

        def  setElemInt(buffer, line, col, band, date):
            buffer.setElem(line, col, band, Integer(date).intValue())

        def  setElemFloat(buffer, line, col, band, date):
            buffer.setElem(line, col, band, Float(date).floatValue())

        def  setElemDouble(buffer, line, col, band, date):
            buffer.setElem(line, col, band, Double(date).doubleValue())

        t = buffer.getDataType()
        if t == Buffer.TYPE_BYTE:
            self.getElem = self.buffer.getElemByte
            self.setElem = setElemByte
        elif t == Buffer.TYPE_SHORT or t == Buffer.TYPE_USHORT:
            self.getElem = self.buffer.getElemShort
            self.setElem = setElemShort
        elif t == Buffer.TYPE_INT:
            self.getElem = self.buffer.getElemInt
            self.setElem = setElemInt
        elif t == Buffer.TYPE_FLOAT:
            self.getElem = self.buffer.getElemFloat
            self.setElem = setElemFloat
        elif t == Buffer.TYPE_DOUBLE:
            self.getElem = self.buffer.getElemDouble
            self.setElem = setElemDouble
        self.values = [0] * self.buffer.getBandCount()
        self.kernel = [[self.values]*3]*3

    def getQuery(self):
        if self.query == None:
            self.prepareQuery()
        return self.query

    def getBuffer(self, store):
        if self.buffer == None:
            self.createBuffer()
            self.prepareBuffer(self.buffer)
        return self.buffer

    def getValue(self, band, row, column):
        if self.getElem == None:
            self.createBuffer()
            self.prepareBuffer(self.buffer)
        return self.getElem(row, column, band)

    def getBandValues(self, row, column):
        if self.getElem == None:
            self.createBuffer()
            self.prepareBuffer(self.buffer)
        for b in xrange(self.buffer.getBandCount()):
            self.values[b] = self.getElem(row, column, b)
        return self.values
    
    def setBandValues(self,row,column,values):
        for b in xrange(self.buffer.getBandCount()):
            self.setElem(self.buffer, row, column, b, values[b])

    def  saveBuffer(self,filename):
        manager = DALLocator.getDataManager ()
        eparams = manager.createServerExplorerParameters(FilesystemServerExplorer.NAME)
        eparams.setDynValue("initialpath","/tmp")
        serverExplorer = manager.openServerExplorer(eparams.getExplorerName(),eparams)

        sparams = serverExplorer.getAddParameters("Gdal Store")
        sparams.setDestination("C:\Users\Sandeep\Desktop","Costa1-B.tif")
        sparams.setBuffer(self.buffer)
        print sparams.getDataStoreName()

        serverExplorer.add("Gdal Store", sparams, True)

## @endcond

##
#
# Represents a raster layer.
#
class RasterLayer(FLyrRaster):
    TYPE_BYTE = Buffer.TYPE_BYTE
    TYPE_SHORT = Buffer.TYPE_SHORT
    TYPE_INT = Buffer.TYPE_INT
    TYPE_FLOAT = Buffer.TYPE_FLOAT
    TYPE_DOUBLE = Buffer.TYPE_DOUBLE

    @staticmethod
    ## @cond FALSE
    def getExtensions(self):
        """This is a internal method, don't use it.
        """
        global rasterLayerExtensions
        extensions = rasterLayerExtensions.get(self.hashCode(), None)
        if extensions ==  None:
            extensions = RasterLayerExtensions(self.getDataStore())
            rasterLayerExtensions[self.hashCode()] = extensions
        return extensions
    ## @endcond

    @staticmethod
    ##
    #
    # Return the number of bands of the raster
    #
    # @return the number of bands of the raster
    #
    def getBandsCount(self):
        return self.getDataStore().getBandCount()

    @staticmethod
    ##
    #
    # Return the width in points of the raster
    #
    # @return the width of the raster
    #
    def getWidth(self):
        return self.getDataStore().getWidth()

    @staticmethod
    ##
    #
    # Return the height in points of the raster
    #
    # @return the height of the raster
    def getHeight(self):
        return self.getDataStore().getHeight()

    @staticmethod
    ##
    #
    # Return the data type of the raster
    #
    # FIXME: Add the documentation about the datatypes
    #
    # @return FIXME
    def getDataType(self):
        return self.getDataStore().getDataType()

    @staticmethod
    ##
    #
    # Return the value of a point of a band for a row/coulmn of
    # the raster.
    #
    # This method use with care, it has a strong overhead. Use instead
    # the method "walk" to go over the raster.
    #
    # @param band band from to retrieve the value
    # @param row FIXME
    # @param column FIXME
    #
    # @return FIXME
    #
    def getData(self, band, row, column):
        return self.getExtensions().getValue(band, row, column)

    @staticmethod
    ##
    #
    # Go over the raster and for each point call to the function
    # "operation" and pass as argument a tuple with the values of
    # the point for each band.
    #
    # This method don't return any value
    #
    # @param operation FIXME
    #
    def walk(self, operation):
        extension =  self.getExtensions()
        store = self.getDataStore()
        for band in xrange(store.getBandCount()):
            for line in xrange(store.getHeight()):
                for column in xrange(store.getWidth()):
                    operation(extension.getBandValues(line, column))

    @staticmethod
    ##
    #
    # DOCUMENT ME !!
    #
    def walkKernel(self, operation):
        extension = self.getExtensions()
        store = self.getDataStore()
        for band in xrange(store.getBandCount()):
            for line in xrange(store.getHeight()):
                for column in xrange(store.getWidth()):
                    values = list()
                    for k in xrange(line-1, line+1):
                        for l in xrange(column-1, column+1):
                            values.append(extension.getBandValues(k,l))
                    operation(values)

    @staticmethod
    ##
    #
    # DOCUMENT ME!!
    #
    def  filter(self, filter1, targetfilename, targetdatatype=None, targetbandcount=None):
        extension = self.getExtensions()
        store = self.getDataStore()
        targetExtension = RasterLayerExtensions()
        targetExtension.createNewBuffer(store.getWidth(),store.getHeight(),targetbandcount,targetdatatype)

        for band in xrange(store.getBandCount()):
            for line in xrange(store.getHeight()):
                for column in xrange(store.getWidth()):
                    values = filter1(extension.getBandValues(line,column))
                    targetExtension.setBandValues(line, column, values)
        targetExtension.saveBuffer(targetfilename)

    @staticmethod
    ##
    #
    # DOCUMENT ME!!
    #
    def filterKernel(self, filter1, targetfilename, targetdatatype):
        pass

    @staticmethod
    ##
    #
    # DOCUMENT ME!!
    #
    def operation(self, operation, layer2, targetfilename, targettype):
        pass

    @staticmethod
    ##
    #
    # DOCUMENT ME !!
    #
    def operationKernel(self, operation, layer2, targetfilename, targettype):
        pass

#
# Inject new methods in the class FLyrRaster
#
FLyrRaster.getExtensions = RasterLayer.getExtensions
FLyrRaster.getBandsCount = RasterLayer.getBandsCount
FLyrRaster.getWidth = RasterLayer.getWidth
FLyrRaster.getHeight = RasterLayer.getHeight
FLyrRaster.getDataType = RasterLayer.getDataType
FLyrRaster.getData = RasterLayer.getData
FLyrRaster.walk = RasterLayer.walk
FLyrRaster.walkKernel = RasterLayer.walkKernel
FLyrRaster.filter =  RasterLayer.filter 
FLyrRaster.filterKernel = RasterLayer.filterKernel
FLyrRaster.operation = RasterLayer.operation
FLyrRaster.operationKernel = RasterLayer.operationKernel

# 
# end module gvsig_raster.py 
# ------------------------------------------ -------------------


#
# Here, code to test the new API.
# 

"""def incrShine(values):
    x = list()
    for value in values:
        x.append(value+20)
    return x

def main():
    layer = loadRasterLayer("/tmp/Costa1.tif")
    layer.filter(incrShine, "/ tmp/Costa1-B.tif" )
"""

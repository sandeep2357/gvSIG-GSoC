from gvsig import *
from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.mapcontext import MapContextLocator
from org.gvsig.fmap.dal.coverage import RasterLocator
from org.gvsig.fmap.dal.coverage.store.parameter import NewRasterStoreParameters
from org.gvsig.fmap.dal.coverage.dataset import Buffer
from org.gvsig.fmap.dal.serverexplorer.filesystem import FilesystemServerExplorer
from org.gvsig.raster.fmap.layers import FLyrRaster
from java.lang import Byte,Short,Integer,Float,Double
from java.io import File
from java.awt.geom import AffineTransform

from os.path import splitext

global sourceFileName
sourceFileName = None

def loadRasterLayer (rasterfile, mode = "r" ):
    ## Load a Raster file in a Layer
    sourceFileName = rasterfile
    if not isinstance (rasterfile,File):
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
rasterLayerExtensions = dict ()


class RasterLayerExtensions(object):
    ##This class hold aditional properties and operations need to manage the scripting raster layer
    def __init__(self, store=None):
        self.store = store
        self.buffer = None
        self.query = None
        self.values = None
        self.kernel = None
        self.setElem = None
        self.getElem = None

    def prepareQuery(self):
        ## See RasterManager in javadocs for more info
        self.query = RasterLocator.getManager().createQuery();
        ## See RasterQuery in javadocs for more
        self.query.setAllDrawableBands()
        self.query.setAreaOfInterest()
        self.buffer = None
        self.values = None
        self.kernel = None

    def loadStore (rasterfile, mode = "r" ):
        if not isinstance (rasterfile,File):
            rasterfile = File(rasterfile)

        name, ext = splitext(rasterfile.getName())

        dalManager = DALLocator.getDataManager()

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
        return dataStore

    def createBuffer(self):
        #print "In createBuffer " + str(sourceFileName)
        if sourceFileName == None:
            self.buffer = self.store.query(self.getQuery())
        else:
            queryStore = self.loadStore(sourceFileName)
            self.buffer = queryStore.query(self.getQuery())
        #print self.buffer.getBandCount()

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

        #print "---->>>>Buffer", datatype, width, height, bandcount
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

        def setElemShort (buffer, line, col, band, data):
            buffer.setElem(line, col, band, Short(data).shortValue())

        def setElemInt(buffer, line, col, band, data):
            buffer.setElem(line, col, band, Integer(data).intValue())

        def setElemFloat(buffer, line, col, band, data):
            buffer.setElem(line, col, band, Float(data).floatValue())

        def setElemDouble(buffer, line, col, band, data):
            buffer.setElem(line, col, band, Double(data).doubleValue())

        t = buffer.getDataType()
        if t == Buffer.TYPE_BYTE:
            self.getElem = buffer.getElemByte
            self.setElem = setElemByte
        elif t == Buffer.TYPE_SHORT or t == Buffer.TYPE_USHORT:
            self.getElem = buffer.getElemShort
            self.setElem = setElemShort
        elif t == Buffer.TYPE_INT:
            self.getElem = buffer.getElemInt
            self.setElem = setElemInt
        elif t == Buffer.TYPE_FLOAT:
            self.getElem = buffer.getElemFloat
            self.setElem = setElemFloat
        elif t == Buffer.TYPE_DOUBLE:
            self.getElem = buffer.getElemDouble
            self.setElem = setElemDouble
        #print buffer.getBandCount()
        self.values = [0] * buffer.getBandCount()
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

    def setValue(self, band, line, col, data):
        t = self.buffer.getDataType()
        if t == Buffer.TYPE_BYTE:
           self.buffer.setElem(line, col, band, Byte(data).byteValue())
        elif t == Buffer.TYPE_SHORT or t == Buffer.TYPE_USHORT:
            self.buffer.setElem(line, col, band, Short(data).shortValue())
        elif t == Buffer.TYPE_INT:
            self.buffer.setElem(line, col, band, Integer(data).intValue())
        elif t == Buffer.TYPE_FLOAT:
            self.buffer.setElem(line, col, band, Float(data).floatValue())
        elif t == Buffer.TYPE_DOUBLE:
            self.buffer.setElem(line, col, band, Double(data).doubleValue())

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

    def saveBuffer(self,filename):
        manager = DALLocator.getDataManager ()
        eparams = manager.createServerExplorerParameters(FilesystemServerExplorer.NAME)
        eparams.setDynValue("initialpath",os.path.dirname(filename))
        serverExplorer = manager.openServerExplorer(eparams.getExplorerName(),eparams)

        sparams = serverExplorer.getAddParameters("Gdal Store")
        sparams.setDestination(os.path.dirname(filename),filename)
        sparams.setBuffer(self.buffer)
        #at = AffineTransform(1, 0, 0, -1, 0, 0)
        #sparams.setAffineTransform(at);
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
        ## This is a internal method, don't use it.

        global rasterLayerExtensions
        extensions = rasterLayerExtensions.get(self.hashCode(), None)
        if extensions == None:
            extensions = RasterLayerExtensions(self.getDataStore())
            rasterLayerExtensions[self.hashCode()] = extensions
        return extensions
    ## @endcond

    @staticmethod
    ##
    #
    # Return the number of bands of the raster
    #
    # @param self The raster layer object
    #
    # @return the number of bands of the raster layer
    #
    def getBandsCount(self):
        return self.getDataStore().getBandCount()

    @staticmethod
    ##
    #
    # Return the width in points/pixels of the raster
    #
    # @param self The raster layer object
    #
    # @return the width of the raster
    #
    def getWidth(self):
        return self.getDataStore().getWidth()

    @staticmethod
    ##
    #
    # Return the height in points/pixels of the raster
    #
    # @param self The raster layer object
    #
    # @return the height of the raster
    def getHeight(self):
        return self.getDataStore().getHeight()

    @staticmethod
    ##
    #
    # Return the data type of the raster
    # TYPE_BYTE = Byte datatype
    # TYPE_USHORT  = Unsigned Short datatype
    # TYPE_SHORT = Signed Short datatype
    # TYPE_INT = Integer datatype
    # TYPE_FLOAT = Float Datatype
    # TYPE_DOUBLE = Double Datatype
    #
    # @param self The raster layer object
    #
    # @return the datatype of the raster layer
    def getDataType(self):
        return self.getDataStore().getDataType()

    @staticmethod
    ##
    #
    # Return the value of a point of a "band" from "row" and "coulmn" of
    # the Raster.
    #
    # This method use with care, it has a strong overhead. Use instead
    # the method "walk" to go over the raster.
    #
    # @param band band from which the value should be retrieved
    # @param row row in the raster from which the value should be retrieved
    # @param column column in the raster from which the value should be retrieved
    #
    # @return the value of a point/pixel of a "band" from "row" and "column" of the Raster
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
    # @param self pointer to the Layer object
    # @param operation any operation which operates on the raster point-by-point
    #
    # @return None
    #
    def walk(self, operation):
        extension = self.getExtensions()
        store = self.getDataStore()
        sourceExtension = RasterLayerExtensions()
        sourceExtension.createNewBuffer(store.getWidth(), store.getHeight(), store.getBandCount(), store.getDataType())
        
        for band in xrange(store.getBandCount()):
            for line in xrange(store.getHeight()):
                for column in xrange(store.getWidth()):
                    operation(extension.getBandValues(line, column))
                    

    @staticmethod
    ##
    #
    # Go over the raster and for each point, taking the neighbour points
    # as a kernel(3x3) call to the function "operation" and pass as argument a
    # tuple with the values of all the points in the kernel for each band.
    #
    # This method don't return any value
    #
    # @param self pointer to the Layer object
    # @param operation any operation which operates on the raster by a kernel(3x3).
    #
    # @return None
    #
    def walkKernel(self, operation):
        extension = self.getExtensions()
        store = self.getDataStore()
        sourceExtension = RasterLayerExtensions()
        sourceExtension.createNewBuffer(store.getWidth(), store.getHeight(), store.getBandCount(), store.getDataType())
        
        k=0
        l=0
        values = [0 for count in xrange(store.getBandCount())]
        values = [[values for count in xrange(3)] for count in xrange(3)]
        outValues = list()
        for band in xrange(store.getBandCount()):
            for line in xrange(1,store.getHeight()-1):
                for column in xrange(1,store.getWidth()-1):
                    
                    i=0
                    for k in xrange(line-1,line+2):
                        j=0
                        for l in xrange(column-1,column+2):
                            #if k>=0 and l>=0 and k<store.getHeight() and l<store.getWidth():
                            values[i][j]=extension.getBandValues(k,l)
                            j=j+1
                        i=i+1
                    operation(values)
                    

    @staticmethod
    ##
    #
    # Go over the raster and for each point call to the function "filter1"
    # and pass as argument a tuple with the values of all the points in the
    # kernel for each band.
    #
    # The function "filter1" must be such that it takes a tuple, modifies its value
    # and returns a new tuple.
    #
    # This method saves the newly created(filter applied) layer to "targetfilename"
    #
    # @param self pointer to the Layer object
    # @param filter1 any filter which modifies the raster layer point-by-point
    # @param targetfilename filename to which the output layer should be saved
    #
    # @return saves the created layer to "targetfilename" in the current directory
    #
    def filter(self, filter1, targetfilename, targetdatatype=None, targetbandcount=None):
        extension = self.getExtensions()
        store = self.getDataStore()
        targetExtension = RasterLayerExtensions()
        #targetExtension.createNewBuffer(store.getWidth(), store.getHeight(), store.getBandCount(), store.getDataType())
        targetExtension.createNewBuffer(store.getWidth(), store.getHeight(), targetbandcount, targetdatatype)

        for band in xrange(store.getBandCount()):
            for line in xrange(store.getHeight()):
                for column in xrange(store.getWidth()):
                    #data = extension.getValue(band, line, column)
                    #data = filter1(data)
                    #targetExtension.setValue(band, line, column, data)
                    values = filter1(extension.getBandValues(line,column))
                    targetExtension.setBandValues(line, column, values)

        targetExtension.saveBuffer(targetfilename)

    @staticmethod
    ##
    #
    # Go over the raster and for each point, taking the neighbour points
    # as a kernel(3x3) call to the function "filter1" and pass as argument
    # a tuple with the values of all the points in the kernel for each band.
    #
    # The function "filter1" must be such that it takes a tuple of multi-dimension,
    # modifies its value and returns a new tuple having dimensions same as input.
    #
    # This method saves the newly created(filter applied) layer to "targetfilename"
    #
    # @param self pointer to the Layer object
    # @param filter1 any filter which modifies the raster layer using a kernel(3x3).
    # @param targetfilename filename to which the output layer should be saved
    #
    # @return saves the created layer to "targetfilename" in the current directory
    #
    def filterKernel(self, filter1, targetfilename, targetdatatype=None, targetbandcount=None):
        extension = self.getExtensions()
        store = self.getDataStore()
        targetExtension = RasterLayerExtensions()
        #targetExtension.createNewBuffer(store.getWidth(), store.getHeight(), store.getBandCount(), store.getDataType())
        targetExtension.createNewBuffer(store.getWidth(), store.getHeight(), targetbandcount, targetdatatype)

        k=0
        l=0
        values = [0 for count in xrange(store.getBandCount())]
        values = [[values for count in xrange(3)] for count in xrange(3)]
        outValues = list()
        for band in xrange(store.getBandCount()):
            for line in xrange(1,store.getHeight()-1):
                for column in xrange(1,store.getWidth()-1):
                    
                    i=0
                    for k in xrange(line-1,line+2):
                        j=0
                        for l in xrange(column-1,column+2):
                            #if k>=0 and l>=0 and k<store.getHeight() and l<store.getWidth():
                            values[i][j]=extension.getBandValues(k,l)
                            j=j+1
                        i=i+1
                    outValues = filter1(values)
                    targetExtension.setBandValues(line, column, outValues)

        targetExtension.saveBuffer(targetfilename)
                    
    @staticmethod
    ##
    #
    # Go over the raster layer and for each point call to the function "operation" and
    # pass as arguments two tuples (One corresponding to the first layer at that point,
    # the other corresponding to the second layer at the same point) with the values of
    # each point for each band.
    #
    # The function "operation" must be such that it takes two tuples as input, performs
    # operations involving both of them and returns a new tuple.
    #
    # This method saves the newly created(from the two rasters) layer to "targetfilename"
    #
    # @param self pointer to the Layer object
    # @param operation any operation which operates on both the raster layers at a respective point/pixel.
    # @param layer2 the layer which forms the second input to the "operation" function.
    # @param targetfilename filename to which the output layer should be saved
    #
    # @return saves the created layer to "targetfilename" in the current directory
    #
    def operation(self, operation, layer2, targetfilename, targetdatatype=None):
        layer1Extension = self.getExtensions()
        layer2Extension = layer2.getExtensions()

        layer1Store = self.getDataStore()
        layer2Store = layer2.getDataStore()

        bandCount = layer1Store.getBandCount()
        layerWidth = layer1Store.getWidth()
        layerHeight = layer1Store.getHeight()
        targetExtension = RasterLayerExtensions()
        targetExtension.createNewBuffer(layerWidth, layerHeight, bandCount, layer1Store.getDataType())

        for band in xrange(bandCount):
            for line in xrange(layerHeight):
                for column in xrange(layerWidth):
                    layer1Values = layer1Extension.getBandValues(line, column)
                    layer2Values = layer2Extension.getBandValues(line, column)
                    resultValues = operation(layer1Values, layer2Values)
                    targetExtension.setBandValues(line, column, resultValues)

        targetExtension.saveBuffer(targetfilename)

    @staticmethod
    ##
    #
    # Go over the raster layer and for each point, taking the neighbour points as a
    # kernel(3x3) call to the function "operation" and pass as arguments two tuples
    # (One corresponding to the first layer at that point, the other corresponding
    # to the second layer at the same point) with the values of all the points of the
    # kernel for each band.
    #
    # The function "operation" must be such that it takes two tuples of multiple
    # dimensions as input, performs operations involving both of them and returns a
    # new tuple having dimensions same as input tuples.
    #
    # This method saves the newly created(from the two rasters) layer to "targetfilename"
    #
    # @param self pointer to the Layer object
    # @param operation any operation which operates on both the raster layers at a respective point/pixel but involving kernel(3x3)[neighbour points].
    # @param layer2 the layer which forms the second input to the "operation" function.
    # @param targetfilename filename to which the output layer should be saved
    #
    # @return saves the created layer to "targetfilename" in the current directory
    #
    def operationKernel(self, operation, layer2, targetfilename, targetdatatype=None):
        layer1Extension = self.getExtensions()
        layer2Extension = self.getExtensions()

        layer1Store = self.getDataStore()
        layer2Store = layer2.getDataStore()

        bandCount = layer1Store.getBandCount()
        layerWidth = layer1Store.getWidth()
        layerHeight = layer1Store.getHeight()
        targetExtension = RasterLayerExtensions()
        targetExtension.createNewBuffer(layerWidth, layerHeight, bandCount, layer1Store.getDataType())

        k=0
        l=0
        values1 = [[[None for count in range(bandCount)] for count in range(3)] for count in range(3)]
        #values1 = [[values1 for count in xrange(3)] 
        values2 = [[[None for count in range(bandCount)] for count in range(3)] for count in range(3)]
        #values2 = [[values2 for count in xrange(3)] for count in xrange(3)]
        #values1 = list()
        #values2 = list()
        tempValues = list()
        outValues = list()
        print bandCount
        for band in xrange(bandCount):
            for line in xrange(1,layerHeight-1):
                for column in xrange(1,layerWidth-1):

                    i=0
                    for k in xrange(line-1,line+2):
                        j=0
                        for l in xrange(column-1,column+2):
                            #if k>=0 and l>=0 and k<store.getHeight() and l<store.getWidth():
                            tempValues=layer1Extension.getBandValues(k,l)
                            values1[i][j]=tempValues
                            print i, j, values1[i][j]
                            print values1
                            values2[i][j]=layer2Extension.getBandValues(k,l)
                            j=j+1
                        i=i+1

                    outValues = operation(values1, values2)
                    i=0
                    for k in xrange(line-1,line+2):
                        j=0
                        for l in xrange(column-1,column+2):
                            targetExtension.setBandValues(k,l, outValues[3*i+j])
                            j=j+1
                        i=i+1

        targetExtension.saveBuffer(targetfilename)
        

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
FLyrRaster.filter = RasterLayer.filter
FLyrRaster.filterKernel = RasterLayer.filterKernel
FLyrRaster.operation = RasterLayer.operation
FLyrRaster.operationKernel = RasterLayer.operationKernel

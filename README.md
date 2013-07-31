<h3>gvSIG-GSoC</h3>


<h3>Add Raster Support to scripting in gvSIG</h3>
<hr/>
The project aim is to implement support for GIS raster data formats in gvSIG 2.0 scripting framework. The scripting extension will be able to let users perform several raster analysis functions (geoprocessing, filters, flow direction analysis etc). By the time of completion of this project, one can work on a wide range of GIS raster data formats in gvSIG 2.0 scripting framework.

For more about the project and work progress refer the <a href='https://github.com/sandeep2357/gvSIG-GSoC/wiki'>wiki page</a>.

<h3>Using the API</h3>
<hr/>
<h4>Requirements</h4>
To be able to work with this API, one must have:
- gvSIG Desktop 2.0
- Scripting Add-on installed in gvSIG 2.0
- gvsig_raster.py file (provided above)

<h4>SetUp</h4>
- First add Raster libraries to the scripting extension. <a href='https://gvsig.org/web/Members/jjdelcerro/gvsig-scripting-raster/adding-the-raster-libraries-to-the-classpath'>See here </a>for help.
- Place a small patch for gvsig.py. <a href='https://gvsig.org/web/Members/jjdelcerro/gvsig-scripting-raster/notas-2/patch-gvsig.py'>See here</a> on how to patch gvsig.py
- Place the downloaded gvsig_raster.py file in [gvsig-install-folder]/gvSIG/extensiones/org.gvsig.scripting.extension/scripting/lib folder.

<h4>Testing</h4>
- Create a view with any name in gvSIG main workspace.
- Open the scripting composer from the gvSIG Tools menu.
- Create a file named loadingRaster.py and place the following in the file.<br/>
<pre>from gvsig import *
from gvsig_raster import *
def main():
        layer = loadRasterLayer('path-to-a-raster-file')</pre>
- Run the script.

<b>Note:</b> If you make any change to gvsig_raster.py file or other files in the lib folder, you need to restart the gvSIG application for the changes to take place.

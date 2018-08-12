import sys
import csv
import getopt

from osgeo import ogr
from osgeo import gdal
from osgeo import osr

def polygonize(raster_path, labels_path, shapefile_path, layer_name='thematic',class_name ='class',id ='id'):
    """ This function converts Raster to shapefile and assigns a class to each polygon according to its pixel value
    Args:
    raster_path(str):the path from which the raster to be converted will be imported
    labels_path(str):the path from which the txt file that contains the labels will be imported
    shapefile_path(str): the path for storing the new shapefile
    layer_name(str):the new shapefile name, defaults to 'thematic'
    class_name(str):the name of the class field, defaults to 'class'
    id(str): the name of the id (this field contains the original pixel value) field,defaults to 'id' """

    #creation of a dictionary for mapping between lables and pixel values:
    open_labeles = open(labels_path)
    reader = csv.reader(open_labeles, delimiter='\n')
    lables_lst = []
    for line in reader:
        lables_lst += line
    lables_dict = {}
    key = 0
    for i in range(len(lables_lst)):
        key += 1
        lables_dict[key] = lables_lst[i]
    # mapping between gdal type and ogr field type:
    type_mapping = {gdal.GDT_Byte: ogr.OFTInteger,gdal.GDT_UInt16: ogr.OFTInteger,gdal.GDT_Int16: ogr.OFTInteger,
                    gdal.GDT_UInt32: ogr.OFTInteger,gdal.GDT_Int32: ogr.OFTInteger,gdal.GDT_Float32: ogr.OFTReal,
                    gdal.GDT_Float64: ogr.OFTReal,gdal.GDT_CInt16: ogr.OFTInteger,gdal.GDT_CInt32: ogr.OFTInteger,
                    gdal.GDT_CFloat32: ogr.OFTReal,gdal.GDT_CFloat64: ogr.OFTReal}

    # get raster data source
    raster_driver = gdal.GetDriverByName('GTiff')
    src_raster = gdal.Open(raster_path)
    input_band = src_raster.GetRasterBand(1)
    # create output data source
    output_shp = shapefile_path
    shp_driver = ogr.GetDriverByName('ESRI Shapefile')
    # create output file name
    output_shapefile = shp_driver.CreateDataSource(output_shp)
    #define output layer srs
    if src_raster.GetProjectionRef() != ' ':
        srs = osr.SpatialReference(src_raster.GetProjectionRef())
        #srs.ImportFromWkt(src_raster.GetProjectionRef())

    dst_layer = output_shapefile.CreateLayer(layer_name, geom_type=ogr.wkbPolygon, srs=srs)

    #add a pixel value field (pixval) and a class field
    raster_field = ogr.FieldDefn(id, type_mapping[input_band.DataType])
    dst_layer.CreateField(raster_field)
    class_field = ogr.FieldDefn(class_name)
    dst_layer.CreateField(class_field)
    # covertion from raster to vector
    gdal.Polygonize(input_band, input_band, dst_layer, 0, [], callback=None)
    dst_layer.SyncToDisk()
    # get new layer
    dataSource = shp_driver.Open(output_shp, 1)
    layer = dataSource.GetLayerByName(layer_name)
    # assignment of a class to each polygon according to its pixel value
    for feature in layer:
        layer.SetFeature(feature)
        pixval = int(feature.GetField(id))
        if pixval in lables_dict:
            feature.SetField(1, lables_dict[pixval])
            layer.SetFeature(feature)
    print('End')




if __name__ == '__main__':

    #opts, args = getopt.getopt(sys.argv[1:], 'rlon', ['raster=', 'labels_path=', 'out_shapefile=', 'layer_name='])
    #layer_name = 'thematic'
    #for opt, val in opts:
        #if (opt in ('-r', '--raster')):
            #raster_path = val
        #elif (opt in ('-l', '--labels_path')):
            #labels_path = val
        #elif (opt in ('-o', '--out_shapefile')):
            #out_shapefile = val
        #elif (opt in ('-n', '--layer_name')):
            #layer_name = val


    raster = '/home/inbal/data/metula/out_supervised2/B_00_01_02_03_FB_00_01_02_03_11_12_33_OR_2.5_CS2.5_20.0_OC_1.0_8.0_CL_32_TF_6_scl_svm__model.svm_OV_0.5_gpu0__llkMap.tif'
    shpfile = '/home/inbal/inbal/gdal/outputs/polygonize'
    lables = '/home/inbal/data/metula/out_supervised2/B_00_01_02_03_FB_00_01_02_03_11_12_33_OR_2.5_CS2.5_20.0_OC_1.0_8.0_CL_32_TF_6_scl_svm__model.svm.lbl'

    polygonize(raster_path=raster, labels_path=lables, shapefile_path=shpfile)






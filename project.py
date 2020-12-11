# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:21:01 2020

@author: JUNHONG
"""

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

#ndvi_2019 = gdal.Open('ndvi_2019.tif')

class cell:
    def __init__(self):
        self.row = 0;
        self.column = 0;
        self.value = [];
    




def read_tif(filename):
    dataset = gdal.Open(filename)
    #print(dataset.RasterCount)#波段数
    im_width = dataset.RasterXSize  #栅格矩阵的列数
    im_height = dataset.RasterYSize  #栅格矩阵的行数
    band=dataset.GetRasterBand(1)
 
    im_geotrans = dataset.GetGeoTransform() #仿射矩阵
    im_proj = dataset.GetProjection() #地图投影信息
    #im_data = band.ReadAsArray(0,0,im_width,im_height) #将数据写成数组，对应栅格矩阵
    im_data = band.ReadAsArray()
 
    del dataset 
    return im_proj,im_geotrans,im_data

def writeTiff(im_data,im_width,im_height,im_bands,im_geotrans,im_proj,path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1,im_data.shape
        #创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    if(dataset!= None):
        dataset.SetGeoTransform(im_geotrans) #写入仿射变换参数
        dataset.SetProjection(im_proj) #写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del dataset

proj_2020, trans_2020, ndvi_2020 = read_tif('ndvi_2020.tif')
proj_2019, trans_2019, ndvi_2019 = read_tif('ndvi_2019.tif')
proj_2018, trans_2018, ndvi_2018 = read_tif('nsw_2018.tif')
proj_2017, trans_2017, ndvi_2017 = read_tif('nsw_2017.tif')
proj_avg, trans_avg,ndvi_avg = read_tif('ndvi_avg.tif')

change_rate = []
cell_list = []
cellmax_change_rate = []

mask_0 = np.logical_and(ndvi_2019<10000,ndvi_2019>0)
mask_0 = np.logical_not(mask_0)
mask_1 = np.logical_and(ndvi_2018<10000,ndvi_2018>0)
mask_1 = np.logical_not(mask_1)
mask_2 = np.logical_and(ndvi_2017<10000,ndvi_2017>0)
mask_2 = np.logical_not(mask_2)
mask_3 = np.logical_and(ndvi_avg<10000,ndvi_avg>0)
mask_3 = np.logical_not(mask_3)
mask_4 = np.logical_and(ndvi_2020<10000,ndvi_2020>0)
mask_4 = np.logical_not(mask_4)

ndvi_2019[mask_0] = 0
ndvi_2018[mask_1] = 0
ndvi_2017[mask_2] = 0
ndvi_avg[mask_3] = 0
ndvi_2020[mask_4] = 0


# for i in range(ndvi_2019.shape[0]):
#     for j in range(ndvi_2019.shape[1]):
#         if(ndvi_avg[i,j]>0):
#             change_rate.append(abs((ndvi_2019[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#             change_rate.append(abs((ndvi_2018[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#             change_rate.append(abs((ndvi_2017[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))

ndvi_2019_c = abs(ndvi_2019-ndvi_avg)/ndvi_avg
ndvi_2018_c = abs(ndvi_2018-ndvi_avg)/ndvi_avg
ndvi_2017_c = abs(ndvi_2017-ndvi_avg)/ndvi_avg

ndvi = np.zeros((ndvi_2017.shape[0],ndvi_2017.shape[1],3))
ndvi[:,:,0] = ndvi_2019_c
ndvi[:,:,1] = ndvi_2018_c
ndvi[:,:,2] = ndvi_2017_c
ndvi_max = np.max(ndvi,-1)

mask = np.logical_and(ndvi_max<10,ndvi_max>-10)
mask = np.logical_not(mask)
ndvi_max[mask] = 0

# for i in range(ndvi_2019.shape[0]):
#     for j in range(ndvi_2019.shape[1]):           
#         cell_list.append(cell())
#         cell_list[i*j+j].row = i
#         cell_list[i*j+j].column = j
#         cell_list[i*j+j].value = []
#         if(ndvi_avg[i,j]>0):
#             cell_list[i*j+j].value.append(abs((ndvi_2019[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#             cell_list[i*j+j].value.append(abs((ndvi_2018[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#             cell_list[i*j+j].value.append(abs((ndvi_2017[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
            
#             change_rate.append(abs((ndvi_2019[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#             change_rate.append(abs((ndvi_2018[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#             change_rate.append(abs((ndvi_2017[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j]))
#         else:
#             cell_list[i*j+j].value.append(0)
#             cell_list[i*j+j].value.append(0)
#             cell_list[i*j+j].value.append(0)

# for index, element in enumerate(cell_list):
#     if(max(element.value)>0):
#         cellmax_change_rate.append(max(element.value))

change_map = ndvi_2020.copy()
rate_threhold = np.percentile(ndvi_max.reshape(-1),97)
for i in range(ndvi_2019.shape[0]):
    for j in range(ndvi_2019.shape[1]):
        if(ndvi_avg[i,j] == 0):
            change_map[i,j] = 0
        elif(abs((ndvi_2019[i,j]-ndvi_avg[i,j])/ndvi_avg[i,j])>rate_threhold):
            change_map[i,j] = 1
        else:
            change_map[i,j] = 0

       
#writeTiff(change_map,change_map.shape[1],change_map.shape[0],1,trans_2020,proj_2020,'change_map_97')

proj_change, trans_change, nsw_change = read_tif('change_map_burn.tif')
proj_burn, trans_burn, nsw_burn = read_tif('nsw_burn_Resample.tif')

mask_5 = np.logical_and(nsw_change<2,nsw_change>-1)
mask_5 = np.logical_not(mask_5)
mask_6 = np.logical_and(nsw_burn<2,nsw_burn>-1)
mask_6 = np.logical_not(mask_6)

nsw_change[mask_5] = 0
nsw_burn[mask_6] = 0

change = change_map.reshape(-1).tolist().count(1)
notchange = change_map.reshape(-1).tolist().count(0)
burn = nsw_burn.reshape(-1).tolist().count(1)
change_burn = 0
change_notburn = 0
notchange_burn = 0
notchange_notburn = 0

for i in range(nsw_change.shape[0]):
    for j in range(nsw_change.shape[1]):
        if(nsw_burn[i,j]== 1):
            if(nsw_change[i,j]==1):
                change_burn = change_burn + 1
            else:
                notchange_burn = notchange_burn + 1
                
change_notburn = change - change_burn
notchange_notburn = notchange - notchange_burn

plt.hist(ndvi_max.reshape(-1).tolist())
plt.title('distribution of max change rate')
plt.xlabel('change rate')
plt.ylabel('amount')


plt.savefig('distribution.png')
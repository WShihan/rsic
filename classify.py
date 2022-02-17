# -*- coding: utf-8 -*-
"""
@Date:  2022-02-14 
@Author:Wang Shihan
"""
from osgeo import  gdal, gdal_array
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import cluster

def preparing(img_file, training_data_file):
    # 读取文件
    img_ds = gdal.Open(img_file, gdal.GA_ReadOnly)
    roi_ds = gdal.Open(training_data_file, gdal.GA_ReadOnly)

    # 转置影像矩阵
    img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
                   gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
    for b in range(img.shape[2]):
        img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()

    roi = roi_ds.GetRasterBand(1).ReadAsArray().astype(np.uint8)
    return img, roi

def filter_data(img, roi):
    # Find how many non-zero entries we have -- i.e. how many training data samples?
    n_samples = (roi > 0).sum()
    print('We have {n} samples'.format(n=n_samples))

    # What are our classification labels?
    labels = np.unique(roi[roi > 0])
    print('The training data include {n} classes: {classes}'.format(
        n=labels.size,classes=labels))
    # We will need a "X" matrix containing our features, and a "y" array containing our labels
    #     These will have n_samples rows
    #     In other languages we would need to allocate these and them loop to fill them, but NumPy can be faster

    X = img[roi > 0, :]  # include 8th band, which is Fmask, for now
    y = roi[roi > 0]
    print('Our X matrix is sized: {sz}'.format(sz=X.shape))
    print('Our y array is sized: {sz}'.format(sz=y.shape))
    # mask
    clear = X[:, 7] <= 1

    X = X[clear, :7]  # we can ditch the Fmask band now
    y = y[clear]
    return X,y

def create_rfc(X, y, img):
    rf = RandomForestClassifier(n_estimators=500, oob_score=True)
    # Fit our model to training data
    rf = rf.fit(X, y)

    # 查看精度
    print('Our OOB prediction of accuracy is: {oob}%'.format(oob=rf.oob_score_ * 100))
    # Take our full image, ignore the Fmask band, and reshape into long 2d array (nrow * ncol, nband) for classification
    new_shape = (img.shape[0] * img.shape[1], img.shape[2] - 1)

    img_as_array = img[:, :, :7].reshape(new_shape)
    print('Reshaped from {o} to {n}'.format(o=img.shape,
                                            n=img_as_array.shape))

    # Now predict for each pixel
    class_prediction = rf.predict(img_as_array)
    # Reshape our classification map
    class_prediction = class_prediction.reshape(img[:, :, 0].shape)
    return class_prediction

def color_stretch(image, index, minmax=(0, 10000)):
    colors = image[:, :, index].astype(np.float64)
    max_val = minmax[1]
    min_val = minmax[0]

    # Enforce maximum and minimum values
    colors[colors[:, :, :] > max_val] = max_val
    colors[colors[:, :, :] < min_val] = min_val

    for b in range(colors.shape[2]):
        colors[:, :, b] = colors[:, :, b] * 1 / (max_val - min_val)
    return colors


def visualize(class_prediction, img):
    img543 = color_stretch(img, [4, 3, 2], (0, 8000))

    # See https://github.com/matplotlib/matplotlib/issues/844/
    n = class_prediction.max()
    # Next setup a colormap for our map
    colors = dict((
        (0, (0, 0, 0, 255)),  # Nodata
        (1, (93, 150, 68, 255)),  # urban
        (2, (0, 255, 0, 255)),  # forest
        (3, (0, 0, 255, 255)),  # water
        (4, (203, 210, 104, 255)),  # field
        (5, (255, 0, 0, 255))  # unknown
    ))

    # Put 0 - 255 as float 0 - 1
    for k in colors:
        v = colors[k]
        _v = [_v / 255.0 for _v in v]
        colors[k] = _v

    index_colors = [colors[key] if key in colors else
                    (255, 255, 255, 0) for key in range(1, n + 1)]
    cmap = plt.matplotlib.colors.ListedColormap(index_colors, 'Classification', n)

    # Now show the classmap next to the image
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    ax[0].imshow(img543)

    ax[1].imshow(class_prediction, cmap=cmap, interpolation='none')

    plt.show()


def main():
    img, label = preparing(r'asset/res/LE70220491999322EDC01_stack.gtif',
                           r'../asset/res/new_qgis_roi.tif')
    X, y = filter_data(img, label)
    class_prediction = create_rfc(X, y,img)
    visualize(class_prediction, img)


# =========================
class K_Means():
    def __init__(self, img_file, count_n, out_file):
        self.n = count_n
        self.img_file = img_file
        self.out_file = out_file
    def classify(self):
        # Read in raster image
        img_ds = gdal.Open(self.img_file, gdal.GA_ReadOnly)

        img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
                       gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
        [self.cols, self.rows] = img[:, :, 0].shape
        self.trans = img_ds.GetGeoTransform()
        self.proj = img_ds.GetProjection()

        for b in range(img.shape[2]):
            img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()
        new_shape = (img.shape[0] * img.shape[1], img.shape[2])
        X = img[:, :, :3].reshape(new_shape)
        k_means = cluster.KMeans(n_clusters=self.n)
        k_means.fit(X)

        X_cluster = k_means.labels_
        X_cluster = X_cluster.reshape(img[:, :, 0].shape)
        return X_cluster

    def save(self, X_cluster):
        driver = gdal.GetDriverByName("GTiff")
        out_img = driver.Create(self.out_file, self.rows, self.cols, 1, gdal.GDT_Byte)
        out_img.SetGeoTransform(self.trans)
        out_img.SetProjection(self.proj)
        out_img.GetRasterBand(1).WriteArray(X_cluster)
        out_img.FlushCache()

    def visualize(self, data):
        pass




if __name__ == '__main__':
    pass





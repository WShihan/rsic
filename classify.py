# -*- coding: utf-8 -*-
"""
@Date:  2022-02-14 
@Author:Wang Shihan
"""
from osgeo import  gdal, gdal_array, ogr
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import cluster
from PyQt5.QtCore import QThread, pyqtSignal

class RfC(QThread):
    signal = pyqtSignal(str)
    sig_cls = pyqtSignal(np.ndarray)
    def __init__(self, file_input, file_out, train_file):
        super(RfC, self).__init__()
        self.file_input = file_input
        self.file_out = file_out
        self.train_file = train_file
        self.preparing()

    def preparing(self):
        img_ds = gdal.Open(self.file_input, gdal.GA_ReadOnly)
        roi_ds = gdal.Open(self.train_file, gdal.GA_ReadOnly)
        self.projection = img_ds.GetProjection()
        self.transform = img_ds.GetGeoTransform()
        self.band_count = img_ds.RasterCount
        self.width = img_ds.RasterXSize
        self.height = img_ds.RasterYSize
        # 转置影像矩阵
        img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
                       gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
        for b in range(img.shape[2]):
            img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()

        self.roi = roi_ds.GetRasterBand(1).ReadAsArray().astype(np.uint8)
        self.img = img
        img_ds = None
        roi_ds = None



    def filter_data(self):
        img, roi = self.img, self.roi
        # Find how many non-zero entries we have -- i.e. how many training data samples?
        n_samples = (roi > 0).sum()
        print('总共有 {n} 条 训练数据'.format(n=n_samples))
        self.signal.emit('总共有 {n} 条 训练数据'.format(n=n_samples))
        # What are our classification labels?
        self.labels = np.unique(roi[roi > 0])

        print('训练数据包含 {n} 个地类: {classes}'.format(n=self.labels.size, classes=self.labels))
        self.signal.emit('训练数据包含 {n} 个地类: {classes}'.format(n=self.labels.size, classes=self.labels))
        # We will need a "X" matrix containing our features, and a "y" array containing our labels
        #     These will have n_samples rows
        #     In other languages we would need to allocate these and them loop to fill them, but NumPy can be faster

        X = img[roi > 0, :]  # include 8th band, which is Fmask, for now
        y = roi[roi > 0]
        """
        print('Our X matrix is sized: {sz}'.format(sz=X.shape))
        print('Our y array is sized: {sz}'.format(sz=y.shape))
        """
        # mask
        #clear = X[:, self.band_count ] <= 1

        #X = X[clear, :7]  # we can ditch the Fmask band now
        #y = y[clear]
        return X, y


    def color_stretch(self, image, index, minmax=(0, 10000)):
        colors = image[:, :, index].astype(np.float64)
        max_val = minmax[1]
        min_val = minmax[0]

        # Enforce maximum and minimum values
        colors[colors[:, :, :] > max_val] = max_val
        colors[colors[:, :, :] < min_val] = min_val

        for b in range(colors.shape[2]):
            colors[:, :, b] = colors[:, :, b] * 1 / (max_val - min_val)
        return colors

    def create_rfc(self):
        X, y = self.filter_data()
        img = self.img
        rf = RandomForestClassifier(n_estimators=500, oob_score=True)
        # Fit our model to training data
        rf = rf.fit(X, y)

        # 查看精度
        print('预测精度为: {oob}%'.format(oob=rf.oob_score_ * 100))
        self.signal.emit('预测精度为: {oob}%'.format(oob=rf.oob_score_ * 100))
        # Take our full image, ignore the Fmask band, and reshape into long 2d array (nrow * ncol, nband) for classification
        new_shape = (img.shape[0] * img.shape[1], img.shape[2])

        img_as_array = img[:, :, : 3].reshape(new_shape)
        # print('Reshaped from {o} to {n}'.format(o=img.shape, n=img_as_array.shape))

        # Now predict for each pixel
        class_prediction = rf.predict(img_as_array)
        # Reshape our classification map
        class_prediction = class_prediction.reshape(img[:, :, 0].shape)
        return class_prediction

    def run(self):
        cls = self.create_rfc()
        self.save(cls)
        self.sig_cls.emit(cls)
    def visualize(self, class_prediction):
        plt.imshow(class_prediction)
        plt.show()
        """
        img = self.img
        img543 = self.color_stretch(img, [4, 3, 2], (0, 8000))
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
        """
    def save(self, X_cluster):
        driver = gdal.GetDriverByName("GTiff")
        out_img = driver.Create(self.file_out, self.width, self.height, 1, gdal.GDT_Byte)
        out_img.SetGeoTransform(self.transform)
        out_img.SetProjection(self.projection)
        out_img.GetRasterBand(1).WriteArray(X_cluster)
        out_img.FlushCache()
        self.signal.emit("--{:-^20}--".format("保存成功"))



# ===============K-Means分类==========
class K_Means(QThread):
    sig_cluster = pyqtSignal(np.ndarray)
    def __init__(self, img_file, count_n,iter_n, out_file):
        super(K_Means, self).__init__()
        self.n = count_n
        self.img_file = img_file
        self.out_file = out_file
    def run(self):
        cluster = self.classify()
        self.save(cluster)
        self.sig_cluster.emit(cluster)

    def classify(self):
        # Read in raster image
        img_ds = gdal.Open(self.img_file, gdal.GA_ReadOnly)

        img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
                       gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
        [self.cols, self.rows] = img[:, :, 0].shape
        self.width = img_ds.RasterXSize
        self.height = img_ds.RasterYSize
        self.trans = img_ds.GetGeoTransform()
        self.proj = img_ds.GetProjection()

        for b in range(img.shape[2]):
            img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()
        new_shape = (img.shape[0] * img.shape[1], img.shape[2])
        X = img[:, :, :3].reshape(new_shape)
        k_means = cluster.KMeans(n_clusters=self.n, max_iter=500)
        k_means.fit(X)

        X_cluster = k_means.labels_
        self.X_cluster = X_cluster.reshape(img[:, :, 0].shape)
        img_ds = None
        return self.X_cluster

    def save(self, X_cluster):
        driver = gdal.GetDriverByName("GTiff")
        out_img = driver.Create(self.out_file, self.width, self.height, 1, gdal.GDT_Byte)
        out_img.SetGeoTransform(self.trans)
        out_img.SetProjection(self.proj)
        out_img.GetRasterBand(1).WriteArray(X_cluster)
        out_img.FlushCache()

    def visualize(self, data):
        plt.imshow(self.X_cluster)
        plt.show()

if __name__ == '__main__':
    rfc = RfC(r'asset/res/LC8_2020.tif', "E:/Desktop/test_lyr.tif", r'./asset/res/jiumo_roi.tif')
    cls = rfc.create_rfc()
    rfc.visualize(cls)

    """
    k = K_Means(r'asset/res/LC8_2020.tif',count_n=5, iter_n=200, out_file="E:/Desktop/test.tif")
    k.classify()
    k.visualize(k.X_cluster)
    """







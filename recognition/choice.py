# -*-coding:utf-8-*-
'''
created by zdd
2019/01/11

choice_R by myself
TF_R by baidu
StuNum_R by xunfei
'''
import numpy as np
import cv2
import os
import imageio
import matplotlib.pyplot as plt
from keras import models
from keras import layers
from PIL import Image, ImageDraw
from skimage import morphology
import time
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error
# os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# choice

'''
input: the path of image
output: numpy.ndarray (x,x,3)
function: get the answer area
'''
model = models.Sequential()
model.add(layers.Conv2D(
    32, (3, 3), activation='relu', input_shape=(60, 60, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.4))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.3))
# model.add(layers.Dense(200, activation='relu'))
model.add(layers.Dense(4, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy', metrics=['accuracy'])
model.load_weights('model/model_weights3.h5')


def the_whole_cutting(img_path):
    img = cv2.imread(img_path)
    print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
    u, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    cnts, hierarchy = cv2.findContours(
        thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)
    c = c[1]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    cv2.drawContours(img.copy(), [box], -1, (0, 0, 255), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    crop_img = img[y1:y1+hight, x1:x1+width]
    img = Image.fromarray(crop_img)
    img.save('process/step1.jpg')
    return crop_img


def get_binary_image_b(img_arr, save_path):
    img = Image.fromarray(img_arr)
    Img = img.convert('L')
    threshold = 150  # 值越大白的越多
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    photo = Img.point(table, '1')
    photo.save(save_path)


def get_binary_image_w(img_arr, save_path):
    img = Image.fromarray(img_arr)
    Img = img.convert('L')
    threshold = 130  # 值越大白的越多
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    photo = Img.point(table, '1')
    photo.save(save_path)


'''
input: image path,save path
function: delete lines
'''


def delete_line(img_path, save_path):
    def dil2ero(img, selem):
        img = morphology.dilation(img, selem)
        imgres = morphology.erosion(img, selem)
        return imgres

    img1 = plt.imread(img_path)
    rows, cols = img1.shape
    col_selem = morphology.rectangle(cols//30, 1)  # 35
    img1_cols = dil2ero(img1, col_selem)
    row_selem = morphology.rectangle(1, rows // 4)  # 6
    img1_rows = dil2ero(img1, row_selem)
    a = img1 - img1_rows+255
    a = a - img1_cols+255
    imageio.imwrite(save_path, a)


'''
input: image path,save path
function: delete noise
'''


def delete_noise(img_path, save_path):
    def getPixel(image, x, y, G, N):
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0
        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            return image.getpixel((x, y-1))
        else:
            return None
    # G: Integer 图像二值化阀值
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功

    def clearNoise(image, G, N, Z):
        draw = ImageDraw.Draw(image)

        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = getPixel(image, x, y, G, N)
                    if color is not None:
                        draw.point((x, y), color)

    image = Image.open(img_path)
    image = image.convert("L")
    clearNoise(image, 50, 2.5, 10)  # 6
    image.save(save_path)


'''
input: numpy.ndarray (x,x)
output: numpy.ndarray (x,x)
function: remove the white hline
'''


def remove_hline(img):
    w = img.shape[0]
    h = img.shape[1]
    count = []
    ll = 0
    row_ids = []

    for i in range(w):
        for j in range(h):
            if img[i, j] > 0:
                ll += 1
        count.append(ll)
        ll = 0

    for k in range(len(count)):
        if count[k] > h*(0.25):
            row_ids.append(k)

    for final in row_ids:
        img.flags.writeable = True
        if final > 0 & final < w-1:
            img[final, :] = 0
            # img[final-1,:]=0
            # img[final+1,:]=0
        if final == 0:
            img[final, :] = 0
            # img[final+1,:]=0
        if final == w-1:
            img[final, :] = 0
            # img[final-1,:]=0
    return img


'''
input: numpy.ndarray (x,x)
output: save to the path(/Users/Nick/Downloads/test/)
function: Generate 20 small images
'''


def small_pieces(img_arr, save_path):
    im = Image.fromarray(img_arr)
    img_size = im.size

    w = img_size[0] / 10.0 - 1
    h = img_size[1] / 2.0 - 1

    for i in range(10):
        x = i*w+2
        y = 0+2
        region = im.crop((x, y, x+w, y+h))
        path = save_path + 'choiceA' + str(i) + '.jpg'
        region.save(path)

    for i in range(10):
        x = i*w+2
        y = h+2
        region = im.crop((x, y, x+w, y+h))
        path = save_path + 'choiceB' + str(i) + '.jpg'
        region.save(path)


def more_accurate(input_path, save_path):
    def single_accurate(path1, path2):
        img = cv2.imread(path1)
        result = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
        (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
        eroded = cv2.erode(closed, kernel)
        contours, hierarchy = cv2.findContours(
            eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        color = (0, 255, 0)
        if len(contours) == 1:
            x, y, w, h = cv2.boundingRect(contours[0])
            x = x - 7
            w = w+14
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            temp = result[y:(y + h), x:(x + w)]
            cv2.imwrite(path2, temp)

        xx = []
        yy = []
        ww = []
        hh = []
        if len(contours) > 1:
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                xx.append(x)
                yy.append(y)
                ww.append(w)
                hh.append(h)
            index = ww.index(max(ww))
            x = xx[index]-7
            y = yy[index]
            w = ww[index]+14
            h = hh[index]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            temp = result[y:(y + h), x:(x + w)]
            cv2.imwrite(path2, temp)

    for filename in os.listdir(input_path):
        if filename != '.DS_Store':
            path1 = input_path + filename
            path2 = save_path + filename
            single_accurate(path1, path2)


'''
input: the path of pred data
output: the input of model
function: propress data
'''


def preprocess_pred_data(path):
    def threchannel21channel(img_path):
        img = Image.open(img_path)
        Img = img.convert('L')
        Img.save(img_path)

    width = 60  # 30
    height = 60
    size = (width, height)
    s = width*height
    real = np.zeros(s).reshape(1, width, height)
    filenames = []
    for filename in os.listdir(path):
        if filename != '.DS_Store':
            filenames.append(filename)
    filenames.sort(reverse=False)

    for filename in filenames:
        path1 = path+filename
        threchannel21channel(path1)
        img = plt.imread(path1)
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        img = img.reshape(1, width, height)
        real = np.vstack((real, img))
        print(filename)
    real_flat = real[1:, :, :].reshape(real.shape[0]-1, -1)
    x_real = real_flat.astype('float32') / 255
    x_real = x_real.reshape(-1, width, height, 1)
    return x_real


'''
input: the path of data and model
output: the pred result
function: pred
'''


def pred(data, model_path):
    global model
    start = time.time()
    a = model.predict(data)
    end = time.time()
    print('识别耗时:'+str(end-start))
    b = np.argmax(a, axis=1)
    c = np.array(['A', 'B', 'C', 'D'])
    d = c[b]
    result = ''.join(list(d))
    return result


def main(img, path, train_path, processed_train_path, model_path):
    # 框出目标轮廓
    start = time.time()
    crop_img = the_whole_cutting(img)
    print('step1--done')
    # 变成白底黑字
    get_binary_image_b(crop_img, path + 'step2.jpg')
    print('step2--done')
    # 去横线
    delete_line(path + 'step2.jpg', path + 'step3.jpg')
    print('step3--done')
    # 去噪声
    sss = time.time()
    delete_noise(path + 'step3.jpg', path + 'step4.jpg')
    eee = time.time()
    print('step4--done')
    print('保存耗时:'+str(eee-sss))

    #  变成黑底白字
    sss = time.time()
    nn = plt.imread(path + 'step4.jpg')
    eee = time.time()
    get_binary_image_w(nn, path + 'step5.jpg')
    print('step5--done')
    print('读取耗时:'+str(eee-sss))
    end = time.time()
    print("预处理耗时:"+str(end-start))
    # 切割成小图
    start = time.time()
    img_arr = plt.imread(path + 'step5.jpg')
    small_pieces(img_arr, train_path)
    print('step6--done')
    # 进一步框出字母
    more_accurate(train_path, processed_train_path)
    print('step7--done')
    # 变成模型需要的输入格式
    x_real = preprocess_pred_data(processed_train_path)
    print('step8--done')
    end = time.time()
    print("分割耗时:"+str(end-start))

    # 预测
    result = pred(x_real, model_path)
    print('step9--done')

    return result


def run_main():

    img_path = 'cqq/1.JPG'
    path = 'process/'
    train_path = 'pred_data/'
    processed_train_path = 'processed_data/'
    model_path = 'model/model_weights3.h5'
    # main(img_path, path, train_path, processed_train_path, model_path)
    start = time.time()
    print(main(img_path, path, train_path, processed_train_path, model_path))
    end = time.time()
    print('总共耗时:'+str(end-start))


run_main()

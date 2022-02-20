# -*-coding:utf-8-*-
import cv2
import numpy as np
import os
from PIL import Image
import urllib.parse
import urllib.request
import base64
import json
import hashlib
import time
import re

def getChoiceAns(index):
	print('getChoice')
	choice_ans0 = ["B", "A", "D", "A", "A", "C", "A", "A", "C", "B", "A", "D", "A", "D", "D", "D", "B", "B", "C", "A"]
	choice_ans1 = ["B", "B", "D", "A", "A", "C", "A", "A", "C", "B", "B", "D", "A", "A", "C", "D", "B", "B", "C", "A"]
	choice_ans2 = ["B", "B", "D", "A", "C", "D", "A", "B", "C", "B", "A", "D", "A", "C", "D", "D", "B", "B", "C", "D"]
	choice_ans = [choice_ans0,choice_ans1,choice_ans2]
	return choice_ans[index]

def getJudgeAns(in_path,imgname,out_path,out_url):
	# 读入原始图像
	print('getJudge')
	origineImage = cv2.imdecode(np.fromfile(
		in_path + '/' + imgname, dtype=np.uint8), -1)
	# 图像灰度化
	image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)
	# 将图片二值化
	retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
	(h, w) = img.shape
	cropImg = img[0:h, 0:w//2]
	saveImg = Image.fromarray(cropImg)
	saveImg.save(out_path + '/judge.jpg')
	return out_url + '/judge.jpg'

def getShortAns(in_path,imgname,out_path,out_url):
	print('getShort')
	origineImage = cv2.imdecode(np.fromfile(
		in_path + '/' + imgname, dtype=np.uint8), -1)
	# 图像灰度化
	image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)
	# 将图片二值化
	retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
	(h, w) = img.shape
	cropImg = img[0:h, w//2:w]
	saveImg = Image.fromarray(cropImg)
	saveImg.save(out_path + '/short.jpg')
	return out_url + '/short.jpg'

def getComputeAns(in_path,imgname1,imgname2,out_path,out_url):
	print('getCompute')
	origineImage1 = cv2.imdecode(np.fromfile(
		in_path + '/' + imgname1, dtype=np.uint8), -1)
	origineImage2 = cv2.imdecode(np.fromfile(
		in_path + '/' + imgname2, dtype=np.uint8), -1)
	# 图像灰度化
	image1 = cv2.cvtColor(origineImage1, cv2.COLOR_BGR2GRAY)
	image2 = cv2.cvtColor(origineImage2, cv2.COLOR_BGR2GRAY)
	# 将图片二值化
	retval, img1 = cv2.threshold(image1, 127, 255, cv2.THRESH_BINARY_INV)
	retval, img2 = cv2.threshold(image2, 127, 255, cv2.THRESH_BINARY_INV)

	(h1, w1) = img1.shape
	(h2, w2) = img2.shape
	cropImg1 = img1[0:h1, 0:w1//2]
	cropImg2 = img1[0:h1, w1 // 2:w1]
	cropImg3 = img2[0:h2, 0:w2 // 2]
	cropImg4 = img2[0:h2, w2 // 2:w2]
	saveImg1 = Image.fromarray(cropImg1)
	saveImg2 = Image.fromarray(cropImg2)
	saveImg3 = Image.fromarray(cropImg3)
	saveImg4 = Image.fromarray(cropImg4)
	saveImg1.save(out_path + '/compute1.jpg')
	saveImg2.save(out_path + '/compute2.jpg')
	saveImg3.save(out_path + '/compute3.jpg')
	saveImg4.save(out_path + '/compute4.jpg')

	return [out_url + '/compute1.jpg',out_url + '/compute2.jpg',out_url + '/compute3.jpg',out_url + '/compute4.jpg']

def xunfei_api(img_path):
    f = open(img_path, 'rb')
    file_content = f.read()
    base64_image = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'image': base64_image})

    url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting'
    api_key = '6d847c604e0cc858d45a34e0173a49d9'
    param = {"language": "cn|en", "location": "true"}

    x_appid = '5cd5acdc'
    x_param = base64.b64encode(json.dumps(
        param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum_contents = api_key + str(x_time) + str(x_param, 'utf-8')
    x_checksum = hashlib.md5(x_checksum_contents.encode('utf-8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url=url, data=body.encode(
        'utf-8'), headers=x_header, method='POST')
    result = urllib.request.urlopen(req)
    result1 = result.read().decode('utf-8')
    reg = r'(.{9})"}]}]}]}'
    wordreg = re.compile(reg)
    wordreglist = re.findall(wordreg, result1)
    return 'U'+wordreglist[0]

def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    # 图像高与宽
    (h, w) = image.shape
    # 长度与图像高度一致的数组
    h_ = [0]*h
    # 循环统计每一行白色像素的个数
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255
    # cv2.imshow('hProjection2', hProjection)
    return h_

def saveProcessedImg(in_path,imgname,out_path):
	# 读入原始图像
	origineImage = cv2.imdecode(np.fromfile(
		in_path + '/' + imgname, dtype=np.uint8), -1)
	# 图像灰度化
	image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)
	# 将图片二值化
	retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
	# cv2.imshow('binary', img)
	# 图像高与宽
	(h, w) = img.shape
	img = img[h // 13:h // 2, 2 * w // 15:w // 2]
	Position = []
	# 水平投影
	H = getHProjection(img)
	# print(H)
	start = 0
	H_Start = []
	H_End = []
	# 根据水平投影获取垂直分割位置
	for i in range(len(H)):
		if H[i] > 0 and start == 0:
			H_Start.append(i)
			start = 1
		if H[i] <= 0 and start == 1:
			H_End.append(i)
			start = 0
	# 分割行，分割之后再进行列分割并保存分割位置
	cropImg = img[H_Start[2]:H_End[2], 0:w]
	saveImg = Image.fromarray(cropImg)
	if not os.path.exists(out_path+'/stu_num'):
		os.makedirs(out_path+'/stu_num')
	saveImg.save(out_path+'/stu_num/'+imgname)
	return out_path+'/stu_num/'+imgname

def getGrades(in_path,out_path,out_url):
	imgs = os.listdir(in_path)
	img_nums = len(imgs)
	grades = []
	i = 0
	while i<img_nums:
		stu_grade = {}
		stu_num_path = saveProcessedImg(in_path, imgs[i], out_path)
		num = xunfei_api(stu_num_path)
		if not os.path.exists(out_path + '/' + num):
			os.makedirs(out_path + '/' + num)
		stu_grade['stu_num'] = num
		stu_grade['choice_ans'] = getChoiceAns(i//4)
		stu_grade['judge_ans'] = getJudgeAns(in_path, imgs[i+1], out_path + '/' + num,out_url + '/' + num)
		stu_grade['short_ans'] = getShortAns(in_path, imgs[i+1], out_path + '/' + num,out_url + '/' + num)
		stu_grade['compute_ans'] = getComputeAns(in_path, imgs[i+2], imgs[i+3], out_path + '/' + num,out_url + '/' + num)
		grades.append(stu_grade)
		i = i+4

	return grades

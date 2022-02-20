# -*- coding:utf-8 -*-
import urllib.parse
import urllib.request
import base64
import json
import hashlib
import time
import re


def xunfei_api(img_path):
    f = open(img_path, 'rb')
    file_content = f.read()
    base64_image = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'image': base64_image})

    url = 'http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting'
    # api_key = 'a54dadd5486c37cd1889507ef0c8cd55'
    api_key = '6d847c604e0cc858d45a34e0173a49d9'
    param = {"language": "cn|en", "location": "true"}

    # x_appid = '5bbaf915'
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
    print(result1)
    reg = r'(.{9})"}]}]}]}'
    wordreg = re.compile(reg)
    wordreglist = re.findall(wordreg, result1)
    print(wordreglist[0])
    return wordreglist[0]


def run_StuNum():
    img_path = 'num.jpg'
    return xunfei_api(img_path)


print(run_StuNum())

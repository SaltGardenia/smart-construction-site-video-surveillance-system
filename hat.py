import json
import cv2
import requests
import os
from apig_sdk import signer

def hat_check(img_path):
    # Config url, ak, sk and file path.
    #https://c1c1a6d2954549e6bee688ed43b2df5b.apig.cn-north-4.huaweicloudapis.com/v1/infers/61807db4-80ff-4273-81e7-2cff9ef78970
    #测试花卉
    url = "https://c1c1a6d2954549e6bee688ed43b2df5b.apig.cn-north-4.huaweicloudapis.com/v1/infers/61807db4-80ff-4273-81e7-2cff9ef78970"
    ak = '7MDT7Q1LQCABCBJQYNHG'
    sk = 'a6xraLfGvr18MAozn3o4f2PQSRPmsHpskEMx3zFJ'
    #花卉测试
    # file_path = "images/down_huahui.jpg"
    file_path = img_path
    # Create request, set method, url, headers and body.
    method = 'POST'
    headers = {"x-sdk-content-sha256": "UNSIGNED-PAYLOAD"}
    request = signer.HttpRequest(method, url, headers)
    # Create sign, set the AK/SK to sign and authenticate the request.
    sig = signer.Signer()
    sig.Key = ak
    sig.Secret = sk
    sig.Sign(request)
    # Send request
    files = {'images': open(file_path, 'rb')}
    resp = requests.request(request.method, request.scheme + "://" + request.host + request.uri, headers=request.headers, files=files)
    '''
    {
        "detection_classes": [
            "white"
        ],
        "detection_boxes": [
            [
                75,
                241,
                275,
                396
            ]
        ],
        "detection_scores": [
            0.9514074325561523
        ]
    }
    解析平台预测出来的数据，
    然后绘制到本地的图片中
    怎么绘制？？
    就是使用openCV绘制内容
    解析数据格式：
        json 格式：{'key':'value','key2':'value2',.....}


    '''
    #解析json格式，获取数据
    date_dict = json.loads(resp.text)
    # print(date_dict)
    return date_dict
    # #获取这个字典里面的数据,因为可以检测多个安全帽，所以是list来储存
    # label_list = date_dict['detection_classes']
    # boxes_list = date_dict['detection_boxes']
    # scores_list = date_dict['detection_scores']
    # print(label_list, boxes_list, scores_list)
    #
    # #使用OpenCV操作图片
    # img = cv2.imread(file_path)
    # #解析
    # for box in boxes_list:
    #     y1, x1, y2, x2 = box[0], box[1], box[2], box[3] #字符串
    #     y1 = int(float(y1))
    #     x1 = int(float(x1))
    #     y2 = int(float(y2))
    #     x2 = int(float(x2))
    #     #绘制矩形     图片    左上角    右下角     颜色      粗细
    #     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
    #
    # cv2.imshow('img', img)
    # cv2.waitKey(0)





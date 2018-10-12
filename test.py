import os
import requests
import time
import cv2


def videoSlice(filename):

    vc = cv2.VideoCapture(os.getcwd()+filename)  # 读入视频文件
    c = 1

    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
    img_dir = './imgs/' + filename.split('/')[2].split('.')[0]+'/'
    time_f = 30  # 视频帧计数间隔频率
    if os.path.isdir(img_dir):
        pass
    else:
        os.mkdir(img_dir)
    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if c % time_f == 0:  # 每隔time_f帧进行存储操作
            cv2.imwrite(img_dir +
                        str(c) + '.jpg', frame)  # 存储为图像
        c = c + 1
        if c > 1000:
            break
        # cv2.waitKey(1)
    vc.release()
    print('video '+ filename.split('/')[2] + ' processed finish')


def uploadImg(dirname, url, cameraId):
    # print(os.listdir(dirname))
    for img in os.listdir(dirname):
        file = {
            'file': open(dirname+'/'+img, 'rb')
        }
        data = {
            'sequenceId': 20181007001,
            'cameraId': cameraId,
            'frame': img.split('.')[0],
        }
        r = requests.post(url, data=data, files=file)
        print(r.text)
    pass


def getTime():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


if __name__ == '__main__':
    # videoSlice(os.getcwd()+'/cameras/1.avi')
    # uploadImg('./imgs/newbx/')
    url = 'http://123.206.79.138:8806/picture/upload'
    # uploadImg('./imgs/tree/',url)
    t1 = time.time()
    for cameras in os.listdir('./cameras'):
        videoSlice('/cameras/' + cameras)
        uploadImg('./imgs/'+cameras.split('.')[0], url, cameraId=cameras.split('.')[0])
    print('finish time:', time.time()-t1, 's')


'''
finish time: 104.55991792678833 s
finish time: 103.50239372253418 s
'''

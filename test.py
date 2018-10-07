import os
import cv2
import requests


def videoSlice(filename):

    vc = cv2.VideoCapture(filename)  # 读入视频文件
    c = 1

    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
    img_dir = './imgs/' + filename.split('.')[0]
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
        # cv2.waitKey(1)
    vc.release()


if __name__ == '__main__':
    videoSlice('newbx.avi')

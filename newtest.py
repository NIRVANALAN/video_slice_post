import os
import requests
import time
import cv2
import queue
import threading

q = queue.Queue(32)


def video_slice(filename, queue):
    vc = cv2.VideoCapture(os.getcwd() + filename)  # 读入视频文件
    c = 1

    if vc.isOpened():  # 判断是否正常打开
        r_val, frame = vc.read()
    else:
        r_val = False
    img_dir = './imgs/' + filename.split('/')[2].split('.')[0] + '/'
    time_f = 30  # 视频帧计数间隔频率
    if os.path.isdir(img_dir):
        pass
    else:
        os.mkdir(img_dir)
    while r_val:  # 循环读取视频帧
        r_val, frame = vc.read()
        if c % time_f == 0:  # 每隔time_f帧进行存储操作
            cv2.imwrite(img_dir + str(c) + '.jpg', frame)  # 存储为图像
        c = c + 1
        if c > 1000:
            break
    # cv2.waitKey(1)
    vc.release()
    print('video ' + filename.split('/')[2] + ' processed finish')
    queue.put(filename.split('/')[2].split('.')[0])


def video_process(queue,):
    for cameras in os.listdir('./cameras'):
        video_slice('/cameras/' + cameras, queue)
        # p = threading.Thread(target=video_slice, args=('/cameras/' + cameras,))


def upload_img(queue, url):
    # print(os.listdir(dirname))
    camera_id = queue.get(1)
    print('get cameraId: ', camera_id)
    dirname = './imgs/' + camera_id
    for img in os.listdir(dirname):
        file = {
            'file': open(dirname + '/' + img, 'rb')
        }
        data = {
            'sequenceId': 20181007001,
            'cameraId': camera_id,
            'frame': img.split('.')[0],
        }
        r = requests.post(url, data=data, files=file)
        print(r.text)
    pass


def upload_process(url, queue, loops):
    for i in range(loops):
        upload_img(queue, url=url)
        time.sleep(1)


def get_time():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def main():
    # videoSlice(os.getcwd()+'/cameras/1.avi')
    # uploadImg('./imgs/newbx/')
    threads = []
    funcs = [video_slice, upload_img]
    nfuncs = range(len(funcs))

    url = 'http://123.206.79.138:8806/picture/upload'
    if not os.path.exists('cameras'):
        os.mkdir('camera')
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    t1 = time.time()

    p = threading.Thread(target=video_process, args=[
                         q], name=video_process.__name__)
    c = threading.Thread(target=upload_process, args=[
                         url, q, len(os.listdir('./cameras'))], name=upload_process.__name__)
    threads.append(p)
    threads.append(c)

    for i in nfuncs:
        threads[i].start()
        print(threads[i].getName() + 'thread start')
    for i in nfuncs:
        threads[i].join()

    print('finish time:', time.time() - t1, 's')


if __name__ == '__main__':
    main()



'''
finish time: 82.94696140289307 s
'''

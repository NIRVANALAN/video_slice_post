import threading
from time import ctime, sleep
import queue

q = queue.Queue(32)


def produce(func):
    for i in range(2):
        # print("I was listening to %s. %s" % (func, ctime()))
        q.put(i, 1)
        print('producing',i, 'size=',q.qsize())
        sleep(1)


def consume(func):
    for i in range(2):
        # print("I was at the %s! %s" % (func, ctime()))
        print('get:',q.get(1))
        sleep(1)


def player(name):
    r = name.split('.')[1]
    if r == 'mp3':
        produce(name)
    else:
        if r == 'mp4':
            consume(name)
        else:
            print('error: The format is not recognized!')


list = ['爱情买卖.mp3', '阿凡达.mp4']
threads = []
files = range(len(list))
# t1 = threading.Thread(target=music, args=('Dying in the sun',))
# t2 = threading.Thread(target=move, args=('Transformers',))
# threads.append(t1)
# threads.append(t2)

for i in files:
    t = threading.Thread(target=player, args=(list[i],))
    threads.append(t)


if __name__ == '__main__':
    # for t in threads:
    #     # 将线程声明为守护线程
    #     t.setDaemon(True)
    #     t.start()
    # t.join()
    # print("All over %s" % ctime())
    for i in files:
        threads[i].start()
        # print('thread name:', threads[i].getName())
    for i in files:
        threads[i].join()
    print("All over %s" % ctime())

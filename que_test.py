import queue
import threading
import time


class BookThread(threading.Thread):
    def __init__(self, thread_id, q, func):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.q = q
        self.func = func

    def run(self):
        print ("线程 %d 开启" % self.threadID)
        # TODO
        process_book(self.threadID, self.q, self.func)
        print ("线程 %d 结束" % self.threadID)


def process_book(thread_id, q, func):
    global existFlag
    while not existFlag:
        queueLock.acquire()
        if not q.empty():
            book = q.get()
            queueLock.release()
            # TODO deal_book
            print ("Thread %d processing book %s" % (thread_id, book))
            func(book)
            time.sleep(1)
        else:
            queueLock.release()


queueLock = threading.Lock()
existFlag = 0


def start_book_threads(book_list, func):
    global existFlag
    existFlag = 0
    thread_list = []
    book_queue = queue.queue()
    # 创建多线程
    for threadID in range(1, THREAD_NUM + 1):
        thread = BookThread(threadID, book_queue, func)
        thread.start()
        thread_list.append(thread)

    # 填充队列
    queueLock.acquire()
    for book in book_list:
        book_queue.put(book)
    queueLock.release()

    # 等待队列清空
    while not book_queue.empty():
        pass

    # 通知线程是时候退出
    existFlag = 1
    print ("book_queue is empty")

    # 等待所有线程完成
    for t in thread_list:
        t.join()

    print ("Exist Main Book Thread")


def deal_book(bk):
    print (bk)


if __name__ == '__main__':
    THREAD_NUM = 3
    bk_list = ['aaa', 'bbb', 'ccc', 'ddd', 'eee',
               'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk']
    start_book_threads(bk_list, deal_book)

import multiprocessing
import os
from multiprocessing import Manager
from multiprocessing import Process
from threading import RLock

content = {}

status = multiprocessing.Array('i', [0])


def load():
    content["A"] = "b"


# 这是一个case：也就是status是公用的，但是content不是，这些进程通过status判断自己不需要加载了，但是其实自己的content还是空的。

def load_test(pid, status, tid=None):
    print(f"{pid}: 未加载", content)

    if not status[0]:
        with RLock():
            if not status[0]:
                print(f"{pid}: I need to load")
                load()
                status[0] = True

    print(f"{pid}: 已加载", content)


def fun1(status):
    pid = os.getpid()
    load_test(pid, status)


if __name__ == '__main__':
    process_list = []
    manager = Manager()
    my_dict = manager.dict()
    for i in range(5):  # 开启5个子进程执行fun1函数
        p = Process(target=fun1, args=(status,))  # 实例化进程对象
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('结束测试')

import os
import threading
from multiprocessing import Manager
from multiprocessing import Process
from sys import stdout
from threading import RLock
from multiprocessing import Lock as PLock

content = {}

status = [0]


def load():
    content["A"] = "b"


# 在这种情况下，每个进程的status都是独立的，所以每个进程都会独立去加载。

def load_test():
    pid = os.getpid()
    tid = threading.current_thread().ident
    if not status[0]:
        with PLock():
            stdout.write(f"{pid}:{tid}: 未加载: {content}\n")
            stdout.flush()
        with RLock():
            if not status[0]:
                with PLock():
                    stdout.write(f"{pid}:{tid}: I need to load\n")
                    stdout.flush()
                load()
                status[0] = True
    with PLock():
        stdout.write(f"{pid}:{tid}: 已加载: {content}\n")
        stdout.flush()


def fun1():
    pid = os.getpid()
    with PLock():
        stdout.write(f"Main PID: {pid}\n")
        stdout.flush()
    tids = []
    for i in range(5):
        t = threading.Thread(target=load_test)
        t.start()
        tids.append(t)
    for t in tids:
        t.join()


if __name__ == '__main__':
    process_list = []
    manager = Manager()
    my_dict = manager.dict()
    for i in range(5):  # 开启5个子进程执行fun1函数
        p = Process(target=fun1, args=())  # 实例化进程对象
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('结束测试')

import time
from multiprocessing import Process, Queue
import numpy as np

# 创建队列
queue = Queue()

def process_1():
    # 在第一个进程中生成图像数据
    for i in range(5):
        image = f"Nihao.img: {i}"
        # 将数据放入队列
        queue.put(image)
        time.sleep(0.5)

def process_2():
    # 在第二个进程中从队列中获取数据
    for i in range(5):
        image = queue.get()
        print(f"Process2: ", image)


# 创建两个进程
p1 = Process(target=process_1)
p2 = Process(target=process_2)

# 启动进程
p1.start()
p2.start()

# 等待进程结束
p1.join()
p2.join()

import ctypes
from multiprocessing import Process, sharedctypes, Queue, Value, Event

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

WIDTH = 1920
HEIGHT = 1080

# 创建一个共享内存变量，类型为 c_int
consumer_is_full = Value('i', 0, lock=False)

# 创建队列
queue = Queue()

# 创建一个事件
producer_event = Event()
consumer_event = Event()

# 创建一个共享内存数组，类型为 c_uint8，形状为 (1920, 1080, 3)
shared_array = sharedctypes.RawArray(ctypes.c_int8, HEIGHT * WIDTH * 3)

# 将共享内存数组转换为 NumPy 数组
np_array = np.frombuffer(shared_array, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))


def process_1():
    # 在第一个进程中生成图像数据
    i = 1
    while True:
        # 等待消费者ready事件
        consumer_event.wait()

        file_name = f'images/image{i}.jpeg'
        print("process 1", file_name)
        with open(file_name, 'rb') as f:
            # 使用 PIL 库的 Image.open 函数将图片加载到内存中
            image = Image.open(f)
            # 使用 numpy 库的 asarray 函数将图片转换为 NumPy 数组
            # 将数据复制到共享内存数组中
            np_array[:] = np.asarray(image)
            queue.put(file_name)

        consumer_event.clear()
        # 设置事件
        producer_event.set()
        i += 1
        if i == 5:
            break


def process_2():
    # 在第二个进程中处理共享内存数组中的数据
    i = 1
    while True:
        # 消费者ready
        consumer_event.set()

        # 等待生产者事件
        producer_event.wait()
        file_name = queue.get()
        print("process 2", file_name)
        image = np_array
        plt.imshow(image)
        plt.show()
        # 清除事件
        producer_event.clear()

        i += 1
        if i == 5:
            break


# 创建两个进程
p1 = Process(target=process_1)
p2 = Process(target=process_2)

# 启动进程
p1.start()
p2.start()

# 等待进程结束
p1.join()
p2.join()

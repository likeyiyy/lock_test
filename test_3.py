import ctypes
from multiprocessing import Process, sharedctypes, Queue

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

WIDTH = 1920
HEIGHT = 1080

# 创建队列
queue = Queue()


# 创建一个共享内存数组，类型为 c_uint8，形状为 (1920, 1080, 3)
shared_array = sharedctypes.RawArray(ctypes.c_int8, HEIGHT * WIDTH * 3)

# 将共享内存数组转换为 NumPy 数组
np_array = np.frombuffer(shared_array, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))


def process_1():
    # 在第一个进程中生成图像数据
    for i in range(1, 5):
        file_name = f'images/image{i}.jpeg'
        with open(file_name, 'rb') as f:
            # 使用 PIL 库的 Image.open 函数将图片加载到内存中
            image = Image.open(f)
            # 使用 numpy 库的 asarray 函数将图片转换为 NumPy 数组
            image_array = np.asarray(image)
            print(image_array.shape)  # 输出图片的形状
            print(image_array.dtype)  # 输出图片的数据类型
            # 将数据复制到共享内存数组中
            np_array[:] = image_array
            queue.put(file_name)


def process_2():
    # 在第二个进程中处理共享内存数组中的数据
    file_name = queue.get()
    print(file_name)
    image = Image.fromarray(np_array)
    plt.imshow(image)
    plt.show()


# 创建两个进程
p1 = Process(target=process_1)
p2 = Process(target=process_2)

# 启动进程
p1.start()
p2.start()

# 等待进程结束
p1.join()
p2.join()

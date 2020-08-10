#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# !@Time     :2019/7/19 10:17
# !@Author   :will
# 進程池

import multiprocessing
import sys


class MyMultiprocessing:
    def __init__(self, pool_size=16):
        if sys.platform == 'win32':
            multiprocessing.freeze_support()  # Windows 平台要加上这句，避免 RuntimeError
        cpu_count = multiprocessing.cpu_count() * 2
        if pool_size > cpu_count:
            pool_size = cpu_count
        print("MyMultiprocessing cpu_count:{}, pool_size:{}".format(cpu_count, pool_size))
        self.pool = multiprocessing.Pool(processes=pool_size)
        self.result = {}

    def add_task(self, task, args, key):
        """
        任务添加到进程池
        :param task:    任务
        :param args:    任务参数,默认不带参数
        :param key:     key必须在当前进程池唯一
        :return:
        """

        result = self.pool.apply_async(task, args)
        self.result[key] = result

    def get_result(self):
        # 获取所有进程結果
        result = {}
        for k, process_result in self.result.items():
            result[k] = process_result.get()
        return result

    def get_result_by_key(self, key):
        # 获取单个子进程的结果
        process_result = self.result.get(key, None)
        return process_result.get() if process_result else None

    def close(self):
        # 获取返回值的过程最好放在进程池回收之后进行，避免阻塞后面的语句
        self.pool.close()
        self.pool.join()


def add(a, b):
    import time
    time.sleep(2)
    return a + b


if __name__ == '__main__':
    mmp = MyMultiprocessing(2)
    for i in range(10):
        mmp.add_task(add, args=(i, i + 1), key=i)

    mmp.close()

    res = mmp.get_result()
    print(res)

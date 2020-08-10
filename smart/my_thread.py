#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# !@Time     :2019/7/19 10:17
# !@Author   :will

import threading


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        return self.result


def add(a, b):
    return a + b


if __name__ == '__main__':
    task = MyThread(add, args=(2, 3))
    task1 = MyThread(add, args=(4, 3, 1))
    task.start()
    task1.start()
    a, b = task.get_result(), task1.get_result()
    print(a, b)

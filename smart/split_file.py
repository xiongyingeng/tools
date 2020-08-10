#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# !@Time     :2019/2/19 15:35
# !@Author   :will

import threading
import time


class Reader(threading.Thread):
    """
    Reader类，继承threading.Thread
    @__init__方法初始化
    @run方法实现了读文件的操作
    """

    def __init__(self, file_name, start_pos, end_pos):
        super(Reader, self).__init__()
        self.file_name = file_name
        self.start_pos = start_pos
        self.end_pos = end_pos

    def run(self):
        fd = open(self.file_name, 'rb')
        '''
        该if块主要判断分块后的文件块的首位置是不是行首，
        是行首的话，不做处理
        否则，将文件块的首位置定位到下一行的行首
        '''
        if self.start_pos != 0:
            fd.seek(self.start_pos - 1)
            txt = fd.read(1)
            if txt != b'\n':
                fd.readline()
                self.start_pos = fd.tell()

        fd.seek(self.start_pos)
        '''
        对该文件块进行处理
        '''
        print(self.start_pos)
        with open(str(self.file_name).rsplit(".", 1)[0] + "_{}_{}.txt".format(self.start_pos, self.end_pos), "w", encoding="utf-8") as wf:
            while self.start_pos <= self.end_pos:
                line = fd.readline().decode().strip()
                self.start_pos = fd.tell()
                wf.write(line + "\n")
        print(self.start_pos, self.end_pos)


class Partition(object):
    """
    对文件进行分块，文件块的数量和线程数量一致
    """

    def __init__(self, file_name, thread_num):
        self.file_name = file_name
        self.block_num = thread_num

    def part(self):
        fd = open(self.file_name, 'r')
        fd.seek(0, 2)
        pos_list = []
        file_size = fd.tell()
        block_size = int(file_size / self.block_num)
        start_pos = 0
        print(file_size)
        for i in range(self.block_num):
            if i == self.block_num - 1:
                end_pos = file_size - 1
                pos_list.append((start_pos, end_pos))
                break
            end_pos = start_pos + block_size - 1
            if end_pos >= file_size:
                end_pos = file_size - 1
            if start_pos >= file_size:
                break
            pos_list.append((start_pos, end_pos))
            start_pos = end_pos + 1
        fd.close()
        return pos_list


if __name__ == '__main__':
    '''
    读取配置文件
    '''

    # 文件名
    file_name = "demo.txt"
    # 线程数量
    thread_num = 7
    # 起始时间
    start_time = time.clock()
    p = Partition(file_name, thread_num)
    t = []
    pos = p.part()
    print(pos)
    # 生成线程
    for i in range(thread_num):
        t.append(Reader(file_name, *pos[i]))
    # 开启线程
    for i in range(thread_num):
        t[i].start()
    for i in range(thread_num):
        t[i].join()
    # 结束时间
    end_time = time.clock()
    print("Cost time is %f" % (end_time - start_time))

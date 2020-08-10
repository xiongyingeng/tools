#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# !@Time     :2018/9/14 15:31
# !@Author   :will
# 文件打包/解包
import os
import sys
from snappy import stream_compress, stream_decompress


class SnappyPacker:
    """
        Snappy解压缩
    """

    @staticmethod
    def stream_compress(src_filename, dst_filename):
        """
        文件压缩
        :param src_filename:    源文件文件名称
        :param dst_filename:    压缩后的文件名称
        :return: 
        """
        with open(src_filename, "rb") as rf, open(dst_filename, "wb") as wf:
            stream_compress(rf, wf)

    @staticmethod
    def stream_decompress(src_filename, dst_filename):
        """
        文件解压
        :param src_filename:    源文件文件名称
        :param dst_filename:    压缩后的文件名称
        :return: 
        """
        with open(src_filename, "rb") as rf, open(dst_filename, "wb") as wf:
            stream_decompress(rf, wf)


def run(root_dir, dst_dir):
    if os.path.isdir(root_dir) and os.path.isdir(root_dir):
        for dirpath, dirnames, filenames in os.walk(root_dir):
            count = len(filenames)
            cur = 0
            for file in filenames:
                cur += 1
                SnappyPacker.stream_compress(os.path.join(dirpath, file), os.path.join(dst_dir, str(file[3:].rsplit(".", 1)[0]) + ".snappy"))
                print("已处理文件:{}, 总共文件:{}".format(cur, count))
    else:
        SnappyPacker.stream_compress(root_dir, str(root_dir.rsplit(".", 1)[0]) + ".snappy")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("*.py filedir filedir2")
        exit(1)

    file_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    if not os.path.exists(file_dir):
        print("file is non-exist")
        exit(2)

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    run(file_dir, dst_dir)

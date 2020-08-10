# -*- coding: utf-8 -*-
# @Time : 2020/7/14 11:40
# @Author : Will
# @Software: PyCharm

import paramiko
import os


def sftp_upload(host, port, username, password, local, remote):
    sf = paramiko.Transport((host, port))
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        if os.path.isdir(local):  # 判断本地参数是目录还是文件
            for f in os.listdir(local):  # 遍历本地目录
                sftp.put(os.path.join(local + f), os.path.join(remote + f))  # 上传目录中的文件
        else:
            sftp.put(local, remote)  # 上传文件
    except Exception as e:
        print('upload exception:', e)
    sf.close()


def sftp_download(host, port, username, password, local, remote):
    sf = paramiko.Transport((host, port))
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        if os.path.isdir(local):  # 判断本地参数是目录还是文件
            for f in sftp.listdir(remote):  # 遍历远程目录
                print(f)
                print(os.path.join(remote + f))
                print(os.path.join(local + f))
                sftp.get(os.path.join(remote + f), os.path.join(local + f))  # 下载目录中文件
        else:
            sftp.get(remote, local)  # 下载文件
    except Exception as e:
        print('download exception:', e)
    sf.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) <= 6:
        print("input: host port username password local remote [222.73.151.246 10022 ubi admin local_path remote_path]")
        exit(-1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]
    local = sys.argv[5]
    remote = sys.argv[6]

    sftp_download(host, port, username, password, local, remote)

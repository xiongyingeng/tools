# -*- coding: utf-8 -*-
# @Time : 2020/7/14 11:31
# @Author : Will
# @Software: PyCharm

from ftplib import FTP_TLS
import os


class FtpDownload:
    def __init__(self, server, port, usrname, pwd):
        self.server = server
        self.port = port
        self.usrname = usrname
        self.pwd = pwd

        self.ftp = self.connect()

    def connect(self):
        print(f"{self.server} {self.port} {self.usrname} {self.pwd}")
        ftp = FTP_TLS()
        try:
            ftp.connect(self.server, self.port)
            ftp.login(self.usrname, self.pwd)
        except:
            raise IOError('\n FTP login failed!!!')
        else:
            print(ftp.getwelcome())
            print('\n+------- FTP connection successful!!! --------+\n')
            return ftp

    def download_file(self, ftpfile, localfile):
        buf_size = 1024
        with open(localfile, 'wb') as fid:
            self.ftp.retrbinary('RETR {0}'.format(ftpfile), fid.write, buf_size)
        return True

    def download_files(self, ftp_path, local_path):
        print('FTP PATH: {0}'.format(ftp_path))
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        self.ftp.cwd(ftp_path)
        print('\n+----------- downloading!!! -----------+\n')
        for i, file in enumerate(self.ftp.nlst()):
            print('{0} <> {1}'.format(i, file))
            local = os.path.join(local_path, file)
            if os.path.isdir(file):  # 判断是否为子目录
                if not os.path.exists(local):
                    os.makedirs(local)
                self.download_files(file, local)
            else:
                self.download_file(file, local)
        self.ftp.cwd('..')

        return True

    def disconnect(self):
        self.ftp.quit()


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

    ftp = FtpDownload(host, port, username, password)
    ftp.download_files(remote, local)
    ftp.disconnect()

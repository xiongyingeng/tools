import hashlib


class SecurityManage:
    """加密管理类"""

    @staticmethod
    def hash_value(value):
        seed = 131
        _hash = 0

        for hx in value:
            _hash = _hash * seed + ord(hx)
        return _hash & 0x7FFFFFFF

    @staticmethod
    def hash_index(src, count):
        """获取哈希取余索引"""
        if count <= 0:
            return 0

        md5_pwd = hashlib.md5(str(src).encode()).hexdigest()[:32]
        index = int(SecurityManage.hash_value(md5_pwd)) % int(count)
        return index

    @staticmethod
    def md5(value):
        return hashlib.md5(str(value).encode()).hexdigest()[:32]


if __name__ == '__main__':
    import sys

    print("Please input device id!!")
    value = sys.argv[1]
    max_count = 2000
    print(SecurityManage.hash_index(value, max_count))

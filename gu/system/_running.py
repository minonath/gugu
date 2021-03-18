import sys
import os

sys.path.append(os.getcwd())

if __name__ == '__main__':  # 可以直接运行此脚本，以单进程运行，但是需要文件夹参数
    from gu.system import gu

    getattr(gu, '_process')()

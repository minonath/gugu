import sys
import os

sys.path.append(os.getcwd())

if __name__ == '__main__':
    from gu.system import gu  # 从新线程启动，必须使用绝对路径。
    getattr(gu, '_new_process')()

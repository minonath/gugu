import sys
import os

sys.path.append(os.getcwd())

if __name__ == '__main__':
    from gu.system import gu
    getattr(gu, '__process__')(debug=True)

import sys
import os

sys.path.append(os.getcwd())

if __name__ == '__main__':
    from gu import gu

    getattr(gu, '_process')()

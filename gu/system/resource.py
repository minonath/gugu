import array
import base64
import os
import random
import struct


_password = (
    b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAY0lEQVR4nO3S2w4AEAwD0P3'
    b'/T/M6kbk100r0cegRYSU5RgbsKBpAv3U9/iwDQKrZAF7NA6Lq6PO9AKxMVIGUbyoHjB9QD9'
    b'id6AG7l/gACviJT0ROMBqAhAH4BTxN51UgI+lABTeXr8GNYKNIAAAAAElFTkSuQmCC'
)


default_png = base64.b64decode(_password)  # 标志图。


def _crypto(data, key):
    random.seed(key)
    data = array.array('B', data)
    length = len(data)
    for i in range(length):
        data[i] ^= random.getrandbits(8) ^ random.getrandbits(3)
    random.seed()
    return data.tobytes(), length


# guru_index, guru_path, guru_get, guru_pack
class _Directory(object):
    """ Gu Resource Unit
    文件夹分布：
    images/     存放图像。
    sounds/     存放音效。
    movies/     存放影像。
    scripts/    存放脚本。
    __meow__.py 启动文件。

    文件存档结构：
    资源段：所有的文件按排序存储，进行加密。
    索引段：上述所有文件的字典，对应字典为（文件名：文件初始位置，文件长度，文件密钥）
    """

    def __init__(self, path):
        self.guru_index = {}
        self.guru_path = os.path.abspath(path)
        self._walk_directory()

    def _walk_directory(self):
        meow = len(self.guru_path) + 1  # 删除前缀用。
        for dir_path, _, file_names in os.walk(self.guru_path):
            for name in file_names:
                name = os.path.join(dir_path, name)[meow:]
                name.replace('\\', '/')  # 统一采用 slash 。
                if '__pycache__' in name:  # 拒绝 python 自带的缓存。
                    continue
                self.guru_index[name] = self.guru_path + '/' + name

    def guru_get(self, name):
        if name not in self.guru_index:
            self._walk_directory()  # 尝试重建缓存。
            if name not in self.guru_index:
                return b''

        path = self.guru_index[name]

        try:
            with open(path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            self._walk_directory()  # 尝试重建缓存。
            return b''

    def guru_pack(self):
        self._walk_directory()  # 重建缓存。
        guru_file = open(self.guru_path + '.guru', 'wb')
        guru_file.write(b'Guru\x00\x00\x00\x00\x00\x00\x00\x00')
        data_index = {}
        start_position = 12

        for target in self.guru_index:  # 这是数据段。
            with open(os.path.join(self.guru_path, target), 'rb') as f:
                data = f.read()
            key = random.getrandbits(32)  # 8-bytes key
            data, data_len = _crypto(data, key)
            guru_file.write(data)
            data_index[target] = (key, start_position, data_len)
            start_position += data_len

        data_info = array.array('B')  # 这是索引段。
        data_name = array.array('B')
        for name, value in data_index.items():
            data_name.extend(name.encode())
            data_name.append(0)
            data_info.extend(_crypto(struct.pack('3I', *value), _password)[0])

        data_name, data_name_len = _crypto(data_name, _password)
        guru_file.write(data_name)
        guru_file.write(data_info.tobytes())
        guru_file.seek(4, 0)
        guru_file.write(struct.pack('2I', start_position, data_name_len))
        guru_file.close()


# guru_index, guru_path, guru_get, guru_unpack, (_guru_file)
class _GuruFile(object):
    def __init__(self, path):
        self.guru_index = {}
        self.guru_path = os.path.abspath(path)
        self._guru_file = open(path, 'rb')
        sign, pos, length = struct.unpack('3I', self._guru_file.read(12))
        assert sign == 1970435399  # b'Guru'
        self._guru_file.seek(pos, 0)
        n = _crypto(self._guru_file.read(length), _password)[0].split(b'\x00')
        k = len(n) - 1
        self.guru_index = dict(
            (n[i].decode(), self._guru_file.read(12)) for i in range(k))

    def __del__(self):
        self._guru_file.close()  # 还没有考虑到不可读文件。

    def guru_get(self, name):
        if name not in self.guru_index:  # 因为打包好了，所以不存在索引缺失。
            return b''

        chunk, length = _crypto(self.guru_index[name], _password)
        assert length == 12
        key, position, length = struct.unpack('3I', chunk)
        self._guru_file.seek(position, 0)
        data = self._guru_file.read(length)
        return _crypto(data, key)[0]

    def guru_unpack(self):
        target_directory, sign = os.path.splitext(self.guru_path)
        assert sign == '.guru'
        for k in self.guru_index:
            path = os.path.join(target_directory, k)
            dir_path = os.path.dirname(path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(path, 'wb') as f:
                f.write(self.guru_get(k))


class Resource(object):
    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return str(self._loaded_order)

    def __init__(self):
        self._default_name = None  # 默认数据单元的名称。
        self._default_guru = None  # 默认数据单元的实例。
        self._loaded_order = []  # 数据单元装载顺序。
        self._gurus_loaded = {}  # 数据单元集合。
        self._files_index = {}  # 所有更新的文件索引。

    def load(self, *path):
        if not path:
            return

        for p in path:
            if not os.path.exists(p):
                p += '.guru'  # 增加默认后缀再次尝试。
                if not os.path.exists(p):
                    continue
                    # raise FileNotFoundError  # 不存在的文件就不会加载。

            self._loaded_order.append(p)  # 加入序列。

            if os.path.isdir(p):  # 文件夹优先。
                directory_or_guru_file = _Directory(p)
            elif os.path.isfile(p):
                directory_or_guru_file = _GuruFile(p)
            else:
                raise OSError  # 一般不存在不是文件也不是文件夹的东西。

            self._gurus_loaded[p] = directory_or_guru_file
            for data_name in directory_or_guru_file.guru_index:
                self._files_index[data_name] = directory_or_guru_file

        self.set_default(self._loaded_order[-1])  # 最后一个加载的设为默认文件。

    def set_default(self, path):
        if path in self._loaded_order:
            self._default_name = path
            self._default_guru = self._gurus_loaded[path]
        else:
            self._default_name = None
            self._default_guru = None

    def unload(self, *path):
        if not path:
            return

        for p in path:
            if p in self._loaded_order:
                self._loaded_order.remove(p)
                self._gurus_loaded.pop(p)

        self._files_index.clear()  # 清空文件索引。

        if self._loaded_order:
            for path_name in self._loaded_order:  # 有顺序重构文件索引。
                directory_or_guru_file = self._gurus_loaded[path_name]
                for data_name in directory_or_guru_file.guru_index:
                    self._files_index[data_name] = directory_or_guru_file

            self.set_default(self._loaded_order[-1])  # 设置默认文件。
        else:
            self.set_default(None)

    def get(self, *name):
        name = '/'.join(name)  # 使用 slash 。
        target_guru = self._files_index.get(name, self._default_guru)
        if not target_guru:
            return b''
        return target_guru.guru_get(name)

    def pack(self):
        if isinstance(self._default_guru, _Directory):
            self._default_guru.guru_pack()

    def unpack(self):
        if isinstance(self._default_guru, _GuruFile):
            self._default_guru.guru_unpack()


__all__ = ['Resource', 'default_png']

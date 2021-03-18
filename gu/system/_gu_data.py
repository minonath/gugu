import array
import base64
import os
import random
import struct

_PY_CACHE = '__py' 'cache__'  # python 文件运行会产生这样的缓存文件夹

_proclaim = (  # 一段明文
    b'iBL{Q4GJ0x0000DNk~Le0000m0000m2nGNE09OL}hX4QokV!;ARCt{2l}ir5AP5D$|E1e)H'
    b'%16w=}f|o!W+}*S^%XyiG{!zf$&p_-ituR-m1`U84z$louNbMF9=j4%A*aP`RpTb>c2+7t4'
    b'9k0-aT4O0v)bY1P~C;F=asDKx={M9t6e<c+Eio0plD5Mhf'
    b'hDb|pdkEdr;-*9cUBKsD-Yl7Bt3OvWARe*ypkUXyu'
    b'qso6++>i_@%07*qoM6N<$f&'
)

_password = base64.b85encode(_proclaim)  # 这是资料文件所采用的密钥

default_png = base64.b85decode(_proclaim)  # 默认的 png 格式图标


def _crypto(data, key):
    """ 加密和解密函数 """

    random.seed(key)  # 设置密钥

    _data = array.array('B', data)  # unsigned integer
    _length = len(_data)

    for _i in range(_length):  # 计算
        _data[_i] ^= random.getrandbits(8) ^ random.getrandbits(3)

    random.seed()  # 重置随机数

    return _data.tobytes(), _length


class _Guru:
    """ 用于资源管理的接口 """

    # guru/
    #     images/         存放图像
    #     sounds/         存放音效
    #     movies/         存放影像
    #     scripts/        存放脚本
    #     __main__.py     启动文件

    def __init__(self, path):
        self.guru_index = {}
        self.guru_path = path

    def guru_get(self, name):
        """ 获取文件的内容 """


class _Directory(_Guru):
    def __init__(self, path):
        _Guru.__init__(self, os.path.abspath(path))

        self.walk_directory()

    def walk_directory(self):
        """ 建立文件目录的缓存 """

        _length = len(self.guru_path) + 1  # 文件夹路径名称的长度，包含斜杠

        for _dir_path, _, _file_names in os.walk(self.guru_path):
            for _name in _file_names:
                # 获取文件相对路径
                _name = os.path.join(_dir_path, _name)[_length:]
                _name.replace('\\', '/')  # 统一替换为 slash
                if _PY_CACHE in _name:  # 跳过 python 自带的缓存
                    continue
                self.guru_index[_name] = self.guru_path + '/' + _name

    def guru_get(self, name):
        if name not in self.guru_index:
            raise IndexError

        _path = self.guru_index[name]

        try:
            with open(_path, 'rb') as _f:
                return _f.read()
        except FileNotFoundError:
            raise IndexError

    def guru_pack(self):
        """
        文件存档结构：
        资源段：所有的文件按排序存储，进行加密
        索引段：上述所有文件的字典，对应字典为（文件名：文件初始位置，文件长度，文件密钥）
        """

        self.walk_directory()  # 重建缓存

        _guru_file = open(self.guru_path + '.guru', 'wb')
        _data_index = {}
        _start_position = 12

        _guru_file.write(b'Guru\x00\x00\x00\x00\x00\x00\x00\x00')  # 写入文件头

        for _target in self.guru_index:  # 这是数据段
            with open(os.path.join(self.guru_path, _target), 'rb') as _f:
                _data = _f.read()
            _key = random.getrandbits(32)  # 8-bytes _key 随机 8 位密码
            _data, _data_len = _crypto(_data, _key)  # 加密
            _guru_file.write(_data)
            _data_index[_target] = _key, _start_position, _data_len  # 记录索引
            _start_position += _data_len

        _data_info = array.array('B')  # 这是索引段
        _data_name = array.array('B')
        for _name, _value in _data_index.items():  # 把记录的文件索引打包成块
            _data_name.extend(_name.encode())
            _data_name.append(0)
            _data_info.extend(
                _crypto(struct.pack('3I', *_value), _password)[0])

        _data_name, data_name_len = _crypto(_data_name, _password)
        _guru_file.write(_data_name)
        _guru_file.write(_data_info.tobytes())

        _guru_file.seek(4, 0)  # 重写文件头
        _guru_file.write(struct.pack('2I', _start_position, data_name_len))

        _guru_file.close()


class _GuruFile(_Guru):
    def __init__(self, path):
        _Guru.__init__(self, os.path.abspath(path))

        if not os.path.exists(path):
            self._guru_file = None
            return

        self._guru_file = open(path, 'rb')
        _sign, _pos, _length = struct.unpack('3I', self._guru_file.read(12))

        assert _sign == 1970435399  # b'Guru'

        self._guru_file.seek(_pos, 0)  # 解压索引段
        _n = _crypto(
            self._guru_file.read(_length), _password)[0].split(b'\x00')
        _k = len(_n) - 1
        self.guru_index = dict(
            (_n[_i].decode(), self._guru_file.read(12)) for _i in range(_k))

    def __del__(self):
        self._guru_file and self._guru_file.close()  # 尝试关闭释放文件

    def guru_get(self, name):
        if name not in self.guru_index:  # 因为打包好了，所以不存在索引缺失
            return b''

        _chunk, _length = _crypto(self.guru_index[name], _password)

        assert _length == 12

        _key, _position, _length = struct.unpack('3I', _chunk)
        self._guru_file.seek(_position, 0)
        data = self._guru_file.read(_length)
        return _crypto(data, _key)[0]

    def guru_unpack(self):
        _target_directory, _sign = os.path.splitext(self.guru_path)

        assert _sign == '.guru'

        for _k in self.guru_index:
            _path = os.path.join(_target_directory, _k)
            _dir_path = os.path.dirname(_path)

            if not os.path.exists(_dir_path):
                os.makedirs(_dir_path)

            with open(_path, 'wb') as _f:
                _f.write(self.guru_get(_k))


class _Resource(object):
    def __repr__(self):
        return 'Resource'

    def __str__(self):
        return str(self._loaded_order)

    def __init__(self):
        self._default_name = None  # 默认数据单元的名称
        self._default_guru = None  # 默认数据单元的实例
        self._loaded_order = []  # 数据单元装载顺序
        self._gurus_loaded = {}  # 数据单元集合
        self._files_index = {}  # 所有更新的文件索引

    def load(self, *path):
        """ 载入资源文件或者目录 """

        for _p in path:
            if not os.path.exists(_p):
                _p += '.guru'  # 增加默认后缀再次尝试
                if not os.path.exists(_p):  # 不存在就不会加载
                    continue  # raise FileNotFoundError

            self._loaded_order.append(_p)  # 加入序列

            if os.path.isdir(_p):  # 文件夹优先
                _guru = _Directory(_p)
            elif os.path.isfile(_p):
                _guru = _GuruFile(_p)
            else:
                raise OSError  # 一般不存在不是文件也不是文件夹的东西

            self._gurus_loaded[_p] = _guru

            for _data_name in _guru.guru_index:
                self._files_index[_data_name] = _guru

        if self._loaded_order:
            self.set_default(self._loaded_order[-1])  # 最后加载的设为默认文件

    def set_default(self, path):
        """ 设置默认文件 """

        if path in self._loaded_order:
            self._default_name = path
            self._default_guru = self._gurus_loaded[path]
        else:
            self._default_name = None
            self._default_guru = None

    def unload(self, *path):
        """ 卸载文件，如果参数为空，等同于刷新索引 """

        for _p in path:
            if _p in self._loaded_order:
                self._loaded_order.remove(_p)
                self._gurus_loaded.pop(_p)

        self._files_index.clear()  # 清空文件索引

        if self._loaded_order:
            self.set_default(self._loaded_order[-1])  # 设置默认文件

            if isinstance(self._default_guru, _Directory):
                self._default_guru.walk_directory()

            for _path_name in self._loaded_order:  # 有顺序重构文件索引
                _guru = self._gurus_loaded[_path_name]
                for data_name in _guru.guru_index:
                    self._files_index[data_name] = _guru

        else:
            self.set_default(None)

    def get(self, *name):
        _name = '/'.join(name)  # 使用 slash
        _target_guru = self._files_index.get(_name, self._default_guru)

        if not _target_guru:
            return b''

        try:
            _result = _target_guru.guru_get(_name)

        except IndexError:  # 出现直接修改文件夹的情况，导致文件多出或者缺失
            self.unload()

            try:
                _result = _target_guru.guru_get(_name)
            except IndexError:
                _result = b''

        return _result

    def pack(self):
        if isinstance(self._default_guru, _Directory):
            self._default_guru.guru_pack()

    def unpack(self):
        if isinstance(self._default_guru, _GuruFile):
            self._default_guru.guru_unpack()

            _guru_name = self._default_name  # 重新载入，以文件夹为主
            self.unload(_guru_name)
            self.load(_guru_name)

    def add(self, *name):
        """ 为默认文件夹添加文件 """

        raise NotImplemented


resource = _Resource()


__all__ = ['default_png', 'resource']

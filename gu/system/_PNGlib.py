import struct
import zlib
import io
import itertools

from ._other import null_function

_HEADER = b'\x49\x48\x44\x52'
_PALETTE = b'\x50\x4c\x54\x45'
_DATA = b'\x49\x44\x41\x54'
_END = b'\x49\x45\x4e\x44'


_COLOR_TYPE_GRAY = 0
_COLOR_TYPE_GRAY_ALPHA = 4
_COLOR_TYPE_PALETTE = 3
_COLOR_TYPE_RGB = 2
_COLOR_TYPE_RGB_ALPHA = 6


def _read_iter(iter_data, size):
    for _ in range(size):
        try:
            yield next(iter_data)
        except StopIteration:
            yield 0


# 这两个函数是通过输入长和宽，来分割当前图像像素的
def _adam7iter(width, height):
    _reduced_order = 0
    _reduced_seven = (
        ((height + 7) // 8, (width + 7) // 8),
        ((height + 7) // 8, (width + 3) // 8),
        ((height + 3) // 8, (width + 3) // 4),
        ((height + 3) // 4, (width + 1) // 4),
        ((height + 1) // 4, (width + 1) // 2),
        ((height + 1) // 2, (width + 0) // 2),
        ((height + 0) // 2, (width + 0) // 1)
    )

    for _reduced_height, _reduced_width in _reduced_seven:
        if _reduced_height and _reduced_width:
            yield _reduced_order

            for _ in range(_reduced_height):
                yield _reduced_width
        _reduced_order -= 1


def _adam1iter(width, height):
    yield 0

    for _ in range(height):
        yield width


_adam7sub1 = (
    0, 5, 3, 5, 1, 5, 3, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    4, 5, 4, 5, 4, 5, 4, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    2, 5, 3, 5, 2, 5, 3, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    4, 5, 4, 5, 4, 5, 4, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
)


def _sub_reconstructor(previous_line, current_line, start_bytes):
    for _i, _j in enumerate(range(start_bytes, len(current_line))):
        _a = current_line[_i]
        _x = current_line[_j]
        current_line[_j] = (_x + _a) & 0xff


def _up_reconstructor(previous_line, current_line, start_bytes):
    for _i in range(len(current_line)):
        _x = current_line[_i]
        _b = previous_line[_i]
        current_line[_i] = (_x + _b) & 0xff


def _average_reconstructor(previous_line, current_line, start_bytes):
    for _i, _j in enumerate(range(len(current_line)), start=-start_bytes):
        _x = current_line[_j]
        if _i < 0:
            _a = 0
        else:
            _a = current_line[_i]
        _b = previous_line[_j]
        current_line[_j] = (_x + ((_a + _b) >> 1)) & 0xff


def _predictor_reconstructor(previous_line, current_line, start_bytes):
    for _i, _j in enumerate(range(len(current_line)), start=-start_bytes):
        _x = current_line[_j]
        if _i < 0:
            _pr = previous_line[_j]
        else:
            _a = current_line[_i]
            _c = previous_line[_i]
            _b = previous_line[_j]
            _pa = abs(_b - _c)
            _pb = abs(_a - _c)
            _pc = abs(_a + _b - _c - _c)
            if _pa <= _pb and _pa <= _pc:
                _pr = _a
            elif _pb <= _pc:
                _pr = _b
            else:
                _pr = _c
        current_line[_j] = (_x + _pr) & 0xff


_reconstruct_function = (null_function, _sub_reconstructor, _up_reconstructor,
                         _average_reconstructor, _predictor_reconstructor)


def _un_filter_image_lines(image_lines, pixel_bytes):
    """ 返回每行的过滤 """
    _previous_line = None

    for _line in image_lines:
        _filter_mode = _line[0]
        _filter_line = _line[1:]

        _reconstruct_function[_filter_mode](
            _previous_line, _filter_line, pixel_bytes
        )
        _previous_line = _filter_line
        yield _filter_line


def _un_interlace(un_filter_images, width, height, pixel_bytes):
    # 下面方法，把每个图片的所有行当成一个一纬数组来看待，也就有 7 个数组
    _reduced = tuple(itertools.chain(*_m) for _m in un_filter_images)

    for _h in range(height):
        _h_1 = (_h % 8) << 3  # 偏移量
        for _w in range(width):
            _image_order = _adam7sub1[_h_1 + _w % 8]  # 当前图像的编号
            _current = _reduced[_image_order]  # 切换数组

            for _ in range(pixel_bytes):  # 从数组里提取多个字节
                yield next(_current)


def read_png(stream):
    if not stream.read(8) == b'\x89PNG\r\n\x1a\n':
        stream.seek(0, 0)  # 重置数据流
        return

    # 读取需要的数据
    _width = _height = _depth = _color_type = _interlace = _pixel_bytes = \
        _palette = None
    _data = []

    while True:
        try:
            _length, _mask = struct.unpack('!I4s', stream.read(8))
            _chunk = stream.read(_length)
            _crc32 = struct.unpack('!I', stream.read(4))[0]

            if zlib.crc32(_mask + _chunk) != _crc32:
                break

            if _mask == _HEADER:
                (_width, _height, _depth, _color_type, _compress_method,
                 _filter_method, _interlace) = struct.unpack('!2I5B', _chunk)

                _planes = (1, -1, 3, 1, 2, -1, 4)[_color_type]
                _pixel_bytes = (_depth * _planes + 7) // 8

            elif _mask == _PALETTE:
                _palette = tuple(
                    _chunk[_i: _i + 3] for _i in range(0, _length, 3))

            elif _mask == _DATA:
                _data.append(_chunk)

            elif _mask == _END:
                break

        except struct.error:
            break

    # LZ77 解压
    _decompress_obj = zlib.decompressobj()
    _unzip_data = itertools.chain(
        *(_decompress_obj.decompress(_chunk) for _chunk in _data),
        _decompress_obj.flush()
    )

    # 按行分割，_adam 表示 pass 提取算法得到的缩小图的每行像素个数
    _adam = (_adam7iter if _interlace else _adam1iter)(_width, _height)
    _reduced_images = tuple([] for _ in range(7 if _interlace else 1))  # 容器
    _current_image = 0  # 不要这个变量也能正常运行

    while True:
        try:
            _line_bytes = next(_adam)
            if _line_bytes > 0:  # 大于 0 表示读取长度
                _reduced_images[_current_image].append(bytearray(
                    # 这是一个从迭代器中依次读取数量个数的方法
                    # 下面的意思是从 _unzip_data 里读取一定数量的字节
                    # 这个字节长度是缩小图每行的字节长度 +1，多出来的是滤波标记
                    _read_iter(_unzip_data, _line_bytes * _pixel_bytes + 1))
                )
            else:  # 小于等于 0 表示切换图片，注意缩小图是 7 张
                _current_image = abs(_line_bytes)

        except StopIteration:
            break

    # 滤波重构
    _un_filter_images = (  # 把多个图片的打包在一起
        # 把一个图片的行打包在一起
        tuple(_un_filter_image_lines(_image_lines, _pixel_bytes))
        for _image_lines in _reduced_images
    )

    # 数据回填
    if _interlace:
        _result = _un_interlace(
            _un_filter_images, _width, _height, _pixel_bytes)
    else:
        _result = itertools.chain(*next(_un_filter_images))  # 这时只有一个图片

    if _depth == 16:  # 要记得放缩深度哦
        _result = (_j for _i, _j in enumerate(_result) if (_i % 2))

    elif _palette:
        _result = itertools.chain(*(_palette[_i] for _i in _result))

    return _width, _height, _color_type, bytes(_result)


def _t_gray_to_rgb_alpha(data, alpha):
    for _i in data:
        yield _i
        yield _i
        yield _i
        yield alpha


def _t_gray_alpha_to_rgb_alpha(data, background):
    while True:
        try:
            _gray, _alpha = next(data), next(data)
            yield background + (_gray - background) * _alpha // 255
        except StopIteration:
            break


def _t_palette_to_rgb(data, palette, alpha, background):
    _br, _bg, _bb = palette[background]
    for _m in data:
        _r, _g, _b = palette[_m]
        _a = alpha[_m]
        yield _br + (_r - _br) * _a // 255
        yield _bg + (_g - _bg) * _a // 255
        yield _bb + (_b - _bb) * _a // 255


def _t_palette_to_rgb_alpha(data, palette, alpha):
    for _m in data:
        _r, _g, _b = palette[_m]
        yield _r
        yield _g
        yield _b
        yield alpha[_m]


def _t_palette_to_rgb2(data, palette):
    for _i in data:
        _r, _g, _b = palette[_i]
        yield _r
        yield _g
        yield _b


def _t_rgb_to_rgb(data, alpha, background):
    _br, _bg, _bb = background
    while True:
        try:
            _r, _g, _b = next(data), next(data), next(data)
            yield _br + (_r - _br) * alpha // 255
            yield _bg + (_g - _bg) * alpha // 255
            yield _bb + (_b - _bb) * alpha // 255
        except StopIteration:
            break


def _t_rgb_to_rgb_alpha(data, alpha):
    while True:
        try:
            yield next(data)
            yield next(data)
            yield next(data)
            yield alpha
        except StopIteration:
            break


def _t_rgb_alpha_to_rgb(data, background):
    _br, _bg, _bb = background
    while True:
        try:
            _r, _g, _b, _a = next(data), next(data), next(data), next(data)
            yield _br + (_r - _br) * _a // 255
            yield _bg + (_g - _bg) * _a // 255
            yield _bb + (_b - _bb) * _a // 255
        except StopIteration:
            break


def read_png2(stream):
    if not stream.read(8) == b'\x89PNG\r\n\x1a\n':
        stream.seek(0, 0)  # 重置数据流
        return

    # 读取需要的数据
    _width = _height = _depth = _color_type = _interlace = _pixel_bytes = \
        _palette = _background = _extra_alpha = None
    _data = []

    while True:
        try:
            _length, _mask = struct.unpack('!I4s', stream.read(8))
            _chunk = stream.read(_length)
            _crc32 = struct.unpack('!I', stream.read(4))[0]

            if zlib.crc32(_mask + _chunk) != _crc32:
                break

            if _mask == _HEADER:
                (_width, _height, _depth, _color_type, _compress_method,
                 _filter_method, _interlace) = struct.unpack('!2I5B', _chunk)

                _planes = (1, -1, 3, 1, 2, -1, 4)[_color_type]
                _pixel_bytes = (_depth * _planes + 7) // 8

            elif _mask == _PALETTE:
                _palette = tuple(
                    _chunk[_i: _i + 3] for _i in range(0, _length, 3))

            elif _mask == _DATA:
                _data.append(_chunk)

            elif _mask == _END:
                break

            elif _mask == b'tRNS':  # 透明信息
                if _color_type == _COLOR_TYPE_GRAY:
                    _extra_alpha = _chunk[1]  # 只取一半
                elif _color_type == _COLOR_TYPE_RGB:  # 只取一半
                    _extra_alpha = _chunk[1], _chunk[3], _chunk[5]
                if _color_type == _COLOR_TYPE_PALETTE:
                    # 这时候是一个 alpha table
                    _length = len(_chunk)
                    _extra_alpha = tuple(_chunk[_i] if _i < _length
                                         else 255 for _i in range(256))

            elif _mask == b'bKGD':
                if _color_type in (_COLOR_TYPE_GRAY, _COLOR_TYPE_GRAY_ALPHA):
                    _background = _chunk[1]
                elif _color_type in (_COLOR_TYPE_RGB, _COLOR_TYPE_RGB_ALPHA):
                    _background = _chunk[1], _chunk[3], _chunk[5]
                elif _color_type == _COLOR_TYPE_PALETTE:
                    _background = ord(_chunk)  # 指向 _palette 不过这里写做代替

        except struct.error:
            break

    # LZ77 解压
    _decompress_obj = zlib.decompressobj()
    _unzip_data = itertools.chain(
        *(_decompress_obj.decompress(_chunk) for _chunk in _data),
        _decompress_obj.flush()
    )

    # 按行分割，_adam 表示 pass 提取算法得到的缩小图的每行像素个数
    _adam = (_adam7iter if _interlace else _adam1iter)(_width, _height)
    _reduced_images = tuple([] for _ in range(7 if _interlace else 1))  # 容器
    _current_image = 0  # 不要这个变量也能正常运行

    while True:
        try:
            _line_bytes = next(_adam)
            if _line_bytes > 0:  # 大于 0 表示读取长度
                _reduced_images[_current_image].append(bytearray(
                    # 这是一个从迭代器中依次读取数量个数的方法
                    # 下面的意思是从 _unzip_data 里读取一定数量的字节
                    # 这个字节长度是缩小图每行的字节长度 +1，多出来的是滤波标记
                    _read_iter(_unzip_data, _line_bytes * _pixel_bytes + 1))
                )
            else:  # 小于等于 0 表示切换图片，注意缩小图是 7 张
                _current_image = abs(_line_bytes)

        except StopIteration:
            break

    # 滤波重构
    _un_filter_images = (  # 把多个图片的打包在一起
        # 把一个图片的行打包在一起
        tuple(_un_filter_image_lines(_image_lines, _pixel_bytes))
        for _image_lines in _reduced_images
    )

    # 数据回填
    if _interlace:
        _result = _un_interlace(
            _un_filter_images, _width, _height, _pixel_bytes)
    else:
        _result = itertools.chain(*next(_un_filter_images))  # 这时只有一个图片

    if _depth == 16:  # 要记得放缩深度哦
        _result = (_j for _i, _j in enumerate(_result) if (_i % 2))

    if _color_type == _COLOR_TYPE_GRAY:
        if _extra_alpha:  # 如果有额外的 alpha 通道
            if _background:  # 把额外通道合并到灰度通道上，这比较简单
                _mode = 'gray'
                _result = (_background + (i - _background) * _extra_alpha
                           // 255 for i in _result)

            else:
                _mode = 'alpha'  # 为了把透明度全部体现
                _result = _t_gray_to_rgb_alpha(_result, _extra_alpha)

        else:  # 不做任何处理
            _mode = 'gray'

    elif _color_type == _COLOR_TYPE_GRAY_ALPHA:
        # 因为已经有了 alpha 通道，所以不关心 _extra_alpha
        _mode = 'alpha'
        _result = _t_gray_alpha_to_rgb_alpha(_result, _background or 0)

    elif _color_type == _COLOR_TYPE_PALETTE:
        if _extra_alpha:
            if _background:
                _mode = 'rgb'
                _result = _t_palette_to_rgb(
                    _result, _palette, _extra_alpha, _background)
            else:
                _mode = 'alpha'
                _result = _t_palette_to_rgb_alpha(
                    _result, _palette, _extra_alpha)

        else:
            _mode = 'rgb'
            _result = _t_palette_to_rgb2(_result, _palette)

    elif _color_type == _COLOR_TYPE_RGB:
        if _extra_alpha:
            if _background:
                _mode = 'rgb'
                _result = _t_rgb_to_rgb(_result, _extra_alpha, _background)

            else:
                _mode = 'alpha'
                _result = _t_rgb_to_rgb_alpha(_result, _extra_alpha)

        else:  # 不做任何处理
            _mode = 'rgb'

    elif _color_type == _COLOR_TYPE_RGB_ALPHA:
        if _background:
            _mode = 'rgb'
            _result = _t_rgb_alpha_to_rgb(_result, _background)
        else:
            _mode = 'alpha'

    else:
        raise

    return _width, _height, _mode, bytes(_result)


# 初版不支持额外的透明信息和背景色
read_png = read_png2


def write_png(width, height, mode, data):
    if mode == 'light':
        _color_type = _COLOR_TYPE_GRAY
        _row_bytes = width
    elif mode == 'rgb':
        _color_type = _COLOR_TYPE_RGB
        _row_bytes = width * 3
    elif mode == 'alpha':
        _color_type = _COLOR_TYPE_RGB_ALPHA
        _row_bytes = width * 4
    else:
        raise

    _head_data = struct.pack('!2I5B', width, height, 8, _color_type, 0, 0, 0)
    _head_crc32 = struct.pack('!I', zlib.crc32(_HEADER + _head_data))

    def _meow():
        _iter_data = iter(data)
        for _ in range(height):
            yield 0
            for _ in range(_row_bytes):
                yield next(_iter_data)

    _filtered_image = bytes(_meow())
    _zipped_image = zlib.compress(_filtered_image)
    _zipped_length = struct.pack('!I', len(_zipped_image))
    _zipped_crc32 = struct.pack('!I', zlib.crc32(_DATA + _zipped_image))

    _result = io.BytesIO()
    _result.write(b'\x89PNG\r\n\x1a\n')
    _result.write(b'\x00\x00\x00\r\x49\x48\x44\x52')
    _result.write(_head_data)
    _result.write(_head_crc32)
    _result.write(_zipped_length)
    _result.write(_DATA)
    _result.write(_zipped_image)
    _result.write(_zipped_crc32)
    _result.write(b'\x00\x00\x00\x00\x49\x45\x4e\x44\xaeB`\x82')

    return _result.getvalue()


def write_png2(width, height, mode, data, data_split=40503):
    if mode == 'light':
        _color_type = _COLOR_TYPE_GRAY
        _row_bytes = width
    elif mode == 'rgb':
        _color_type = _COLOR_TYPE_RGB
        _row_bytes = width * 3
    elif mode == 'alpha':
        _color_type = _COLOR_TYPE_RGB_ALPHA
        _row_bytes = width * 4
    else:
        raise

    _head_data = struct.pack('!2I5B', width, height, 8, _color_type, 0, 0, 0)
    _head_crc32 = struct.pack('!I', zlib.crc32(_HEADER + _head_data))

    _filtered_image = io.BytesIO()

    for _i in range(0, len(data), _row_bytes):
        _filtered_image.write(b'\x00')
        _filtered_image.write(data[_i: _i + _row_bytes])

    _zipped_data = zlib.compress(_filtered_image.getvalue())
    _split_data = (_zipped_data[i: i + data_split]
                   for i in range(0, len(_zipped_data), data_split))

    _result = io.BytesIO()
    _result.write(b'\x89PNG\r\n\x1a\n')
    _result.write(b'\x00\x00\x00\r\x49\x48\x44\x52')
    _result.write(_head_data)
    _result.write(_head_crc32)

    for _s_data in _split_data:
        _s_length = struct.pack('!I', len(_s_data))
        _s_crc32 = struct.pack('!I', zlib.crc32(_DATA + _s_data))

        _result.write(_s_length)
        _result.write(_DATA)
        _result.write(_s_data)
        _result.write(_s_crc32)

    _result.write(b'\x00\x00\x00\x00\x49\x45\x4e\x44\xaeB`\x82')

    return _result.getvalue()


# 初版不支持 256 * 256 以上的信息
write_png = write_png2


__all__ = ['read_png', 'write_png']

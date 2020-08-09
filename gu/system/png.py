import struct
import zlib
import io
import itertools

HEADER = b'\x49\x48\x44\x52'
PALETTE = b'\x50\x4c\x54\x45'
DATA = b'\x49\x44\x41\x54'
END = b'\x49\x45\x4e\x44'


COLOR_TYPE_GRAY = 0
COLOR_TYPE_GRAY_ALPHA = 4
COLOR_TYPE_PALETTE = 3
COLOR_TYPE_RGB = 2
COLOR_TYPE_RGB_ALPHA = 6


def read_iterator(iter_data, size):
    for _ in range(size):
        try:
            yield next(iter_data)
        except StopIteration:
            yield 0


# 这两个函数是通过输入长和宽，来分割当前图像像素的
def adam7iter(width, height):
    reduced_order = 0
    reduced_seven = (
        ((height + 7) // 8, (width + 7) // 8),
        ((height + 7) // 8, (width + 3) // 8),
        ((height + 3) // 8, (width + 3) // 4),
        ((height + 3) // 4, (width + 1) // 4),
        ((height + 1) // 4, (width + 1) // 2),
        ((height + 1) // 2, (width + 0) // 2),
        ((height + 0) // 2, (width + 0) // 1)
    )

    for reduced_height, reduced_width in reduced_seven:
        if reduced_height and reduced_width:
            yield reduced_order

            for _ in range(reduced_height):
                yield reduced_width
        reduced_order -= 1


def adam1iter(width, height):
    yield 0

    for _ in range(height):
        yield width


adam7sub1 = (
    0, 5, 3, 5, 1, 5, 3, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    4, 5, 4, 5, 4, 5, 4, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    2, 5, 3, 5, 2, 5, 3, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
    4, 5, 4, 5, 4, 5, 4, 5,
    6, 6, 6, 6, 6, 6, 6, 6,
)


def do_nothing(*args):
    pass


def sub_reconstructor(previous_line, current_line, start_bytes):
    for i, j in enumerate(range(start_bytes, len(current_line))):
        a = current_line[i]
        x = current_line[j]
        current_line[j] = (x + a) & 0xff


def up_reconstructor(previous_line, current_line, start_bytes):
    for i in range(len(current_line)):
        x = current_line[i]
        b = previous_line[i]
        current_line[i] = (x + b) & 0xff


def average_reconstructor(previous_line, current_line, start_bytes):
    for i, j in enumerate(range(len(current_line)), start=-start_bytes):
        x = current_line[j]
        if i < 0:
            a = 0
        else:
            a = current_line[i]
        b = previous_line[j]
        current_line[j] = (x + ((a + b) >> 1)) & 0xff


def predictor_reconstructor(previous_line, current_line, start_bytes):
    for i, j in enumerate(range(len(current_line)), start=-start_bytes):
        x = current_line[j]
        if i < 0:
            pr = previous_line[j]
        else:
            a = current_line[i]
            c = previous_line[i]
            b = previous_line[j]
            pa = abs(b - c)
            pb = abs(a - c)
            pc = abs(a + b - c - c)
            if pa <= pb and pa <= pc:
                pr = a
            elif pb <= pc:
                pr = b
            else:
                pr = c
        current_line[j] = (x + pr) & 0xff


reconstruct_function = (do_nothing, sub_reconstructor, up_reconstructor,
                        average_reconstructor, predictor_reconstructor)


def un_filter_image_lines(image_lines, pixel_bytes):
    """ 返回每行的过滤 """
    previous_line = None

    for line in image_lines:
        filter_mode = line[0]
        filter_line = line[1:]

        reconstruct_function[filter_mode](
            previous_line, filter_line, pixel_bytes
        )
        previous_line = filter_line
        yield filter_line


def un_interlace(un_filter_images, width, height, pixel_bytes):
    # 下面方法，把每个图片的所有行当成一个一纬数组来看待，也就有 7 个数组
    reduced = tuple(itertools.chain(*m) for m in un_filter_images)

    for h in range(height):
        h_1 = (h % 8) << 3  # 偏移量
        for w in range(width):
            image_order = adam7sub1[h_1 + w % 8]  # 当前图像的编号
            current = reduced[image_order]  # 切换数组

            for _ in range(pixel_bytes):  # 从数组里提取多个字节
                yield next(current)


def read_png(stream):
    if not stream.read(8) == b'\x89PNG\r\n\x1a\n':
        stream.seek(0, 0)  # 重置数据流
        return

    # 读取需要的数据
    width = height = depth = color_type = interlace = pixel_bytes = \
        palette = None
    data = []

    while True:
        try:
            length, mask = struct.unpack('!I4s', stream.read(8))
            chunk = stream.read(length)
            crc32 = struct.unpack('!I', stream.read(4))[0]

            if zlib.crc32(mask + chunk) != crc32:
                break

            if mask == HEADER:
                (width, height, depth, color_type, compress_method,
                 filter_method, interlace) = struct.unpack('!2I5B', chunk)

                planes = (1, -1, 3, 1, 2, -1, 4)[color_type]
                pixel_bytes = (depth * planes + 7) // 8

            elif mask == PALETTE:
                palette = tuple(
                    chunk[i: i + 3] for i in range(0, length, 3))

            elif mask == DATA:
                data.append(chunk)

            elif mask == END:
                break

        except struct.error:
            break

    # LZ77 解压
    decompress_obj = zlib.decompressobj()
    unzip_data = itertools.chain(
        *(decompress_obj.decompress(chunk) for chunk in data),
        decompress_obj.flush()
    )

    # 按行分割，adam 表示 pass 提取算法得到的缩小图的每行像素个数
    adam = (adam7iter if interlace else adam1iter)(width, height)
    reduced_images = tuple([] for _ in range(7 if interlace else 1))  # 容器
    current_image = 0  # 不要这个变量也能正常运行

    while True:
        try:
            line_bytes = next(adam)
            if line_bytes > 0:  # 大于 0 表示读取长度
                reduced_images[current_image].append(bytearray(
                    # 这是一个从迭代器中依次读取数量个数的方法
                    # 下面的意思是从 unzip_data 里读取一定数量的字节
                    # 这个字节长度是缩小图每行的字节长度 +1，多出来的是滤波标记
                    read_iterator(unzip_data, line_bytes * pixel_bytes + 1))
                )
            else:  # 小于等于 0 表示切换图片，注意缩小图是 7 张
                current_image = abs(line_bytes)

        except StopIteration:
            break

    # 滤波重构
    un_filter_images = (  # 把多个图片的打包在一起
        # 把一个图片的行打包在一起
        tuple(un_filter_image_lines(image_lines, pixel_bytes))
        for image_lines in reduced_images
    )

    # 数据回填
    if interlace:
        result = un_interlace(un_filter_images, width, height, pixel_bytes)
    else:
        result = itertools.chain(*next(un_filter_images))  # 这时只有一个图片

    if depth == 16:  # 要记得放缩深度哦
        result = (j for i, j in enumerate(result) if (i % 2))

    elif palette:
        result = itertools.chain(*(palette[i] for i in result))

    return width, height, color_type, bytes(result)


def t_gray_to_rgb_alpha(data, alpha):
    for i in data:
        yield i
        yield i
        yield i
        yield alpha


def t_gray_alpha_to_rgb_alpha(data, background):
    while True:
        try:
            gray, alpha = next(data), next(data)
            yield background + (gray - background) * alpha // 255
        except StopIteration:
            break


def t_palette_to_rgb(data, palette, alpha, background):
    br, bg, bb = palette[background]
    for m in data:
        rr, rg, rb = palette[m]
        ra = alpha[m]
        yield br + (rr - br) * ra // 255
        yield bg + (rg - bg) * ra // 255
        yield bb + (rb - bb) * ra // 255


def t_palette_to_rgb_alpha(data, palette, alpha):
    for m in data:
        rr, rg, rb = palette[m]
        yield rr
        yield rg
        yield rb
        yield alpha[m]


def t_palette_to_rgb2(data, palette):
    for i in data:
        rr, rg, rb = palette[i]
        yield rr
        yield rg
        yield rb


def t_rgb_to_rgb(data, alpha, background):
    br, bg, bb = background
    while True:
        try:
            rr, rg, rb = next(data), next(data), next(data)
            yield br + (rr - br) * alpha // 255
            yield bg + (rg - bg) * alpha // 255
            yield bb + (rb - bb) * alpha // 255
        except StopIteration:
            break


def t_rgb_to_rgb_alpha(data, alpha):
    while True:
        try:
            yield next(data)
            yield next(data)
            yield next(data)
            yield alpha
        except StopIteration:
            break


def t_rgb_alpha_to_rgb(data, background):
    br, bg, bb = background
    while True:
        try:
            rr, rg, rb, ra = next(data), next(data), next(data), next(data)
            yield br + (rr - br) * ra // 255
            yield bg + (rg - bg) * ra // 255
            yield bb + (rb - bb) * ra // 255
        except StopIteration:
            break


def read_png2(stream):
    if not stream.read(8) == b'\x89PNG\r\n\x1a\n':
        stream.seek(0, 0)  # 重置数据流
        return

    # 读取需要的数据
    width = height = depth = color_type = interlace = pixel_bytes = \
        palette = background = extra_alpha = None
    data = []

    while True:
        try:
            length, mask = struct.unpack('!I4s', stream.read(8))
            chunk = stream.read(length)
            crc32 = struct.unpack('!I', stream.read(4))[0]

            if zlib.crc32(mask + chunk) != crc32:
                break

            if mask == HEADER:
                (width, height, depth, color_type, compress_method,
                 filter_method, interlace) = struct.unpack('!2I5B', chunk)

                planes = (1, -1, 3, 1, 2, -1, 4)[color_type]
                pixel_bytes = (depth * planes + 7) // 8

            elif mask == PALETTE:
                palette = tuple(
                    chunk[i: i + 3] for i in range(0, length, 3))

            elif mask == DATA:
                data.append(chunk)

            elif mask == END:
                break

            elif mask == b'tRNS':  # 透明信息
                if color_type == COLOR_TYPE_GRAY:
                    extra_alpha = chunk[1]  # 只取一半
                elif color_type == COLOR_TYPE_RGB:  # 只取一半
                    extra_alpha = chunk[1], chunk[3], chunk[5]
                if color_type == COLOR_TYPE_PALETTE:
                    # 这时候是一个 alpha table
                    length = len(chunk)
                    extra_alpha = tuple(
                        chunk[i] if i < length else 255 for i in range(256)
                    )

            elif mask == b'bKGD':
                if color_type in (COLOR_TYPE_GRAY, COLOR_TYPE_GRAY_ALPHA):
                    background = chunk[1]
                elif color_type in (COLOR_TYPE_RGB, COLOR_TYPE_RGB_ALPHA):
                    background = chunk[1], chunk[3], chunk[5]
                elif color_type == COLOR_TYPE_PALETTE:
                    background = ord(chunk)  # 指向 palette 不过这里写做代替

        except struct.error:
            break

    # LZ77 解压
    decompress_obj = zlib.decompressobj()
    unzip_data = itertools.chain(
        *(decompress_obj.decompress(chunk) for chunk in data),
        decompress_obj.flush()
    )

    # 按行分割，adam 表示 pass 提取算法得到的缩小图的每行像素个数
    adam = (adam7iter if interlace else adam1iter)(width, height)
    reduced_images = tuple([] for _ in range(7 if interlace else 1))  # 容器
    current_image = 0  # 不要这个变量也能正常运行

    while True:
        try:
            line_bytes = next(adam)
            if line_bytes > 0:  # 大于 0 表示读取长度
                reduced_images[current_image].append(bytearray(
                    # 这是一个从迭代器中依次读取数量个数的方法
                    # 下面的意思是从 unzip_data 里读取一定数量的字节
                    # 这个字节长度是缩小图每行的字节长度 +1，多出来的是滤波标记
                    read_iterator(unzip_data, line_bytes * pixel_bytes + 1))
                )
            else:  # 小于等于 0 表示切换图片，注意缩小图是 7 张
                current_image = abs(line_bytes)

        except StopIteration:
            break

    # 滤波重构
    un_filter_images = (  # 把多个图片的打包在一起
        # 把一个图片的行打包在一起
        tuple(un_filter_image_lines(image_lines, pixel_bytes))
        for image_lines in reduced_images
    )

    # 数据回填
    if interlace:
        result = un_interlace(un_filter_images, width, height, pixel_bytes)
    else:
        result = itertools.chain(*next(un_filter_images))  # 这时只有一个图片

    if depth == 16:  # 要记得放缩深度哦
        result = (j for i, j in enumerate(result) if (i % 2))

    if color_type == COLOR_TYPE_GRAY:
        if extra_alpha:  # 如果有额外的 alpha 通道
            if background:  # 把额外通道合并到灰度通道上，这比较简单
                mode = 'gray'
                result = (background + (i - background) * extra_alpha // 255
                          for i in result)

            else:
                mode = 'alpha'  # 为了把透明度全部体现
                result = t_gray_to_rgb_alpha(result, extra_alpha)

        else:  # 不做任何处理
            mode = 'gray'

    elif color_type == COLOR_TYPE_GRAY_ALPHA:
        # 因为已经有了 alpha 通道，所以不关心 extra_alpha
        mode = 'alpha'
        result = t_gray_alpha_to_rgb_alpha(result, background or 0)

    elif color_type == COLOR_TYPE_PALETTE:
        if extra_alpha:
            if background:
                mode = 'rgb'
                result = t_palette_to_rgb(
                    result, palette, extra_alpha, background
                )
            else:
                mode = 'alpha'
                result = t_palette_to_rgb_alpha(result, palette, extra_alpha)

        else:
            mode = 'rgb'
            result = t_palette_to_rgb2(result, palette)

    elif color_type == COLOR_TYPE_RGB:
        if extra_alpha:
            if background:
                mode = 'rgb'
                result = t_rgb_to_rgb(result, extra_alpha, background)

            else:
                mode = 'alpha'
                result = t_rgb_to_rgb_alpha(result, extra_alpha)

        else:  # 不做任何处理
            mode = 'rgb'

    elif color_type == COLOR_TYPE_RGB_ALPHA:
        if background:
            mode = 'rgb'
            result = t_rgb_alpha_to_rgb(result, background)
        else:
            mode = 'alpha'

    else:
        raise

    return width, height, mode, bytes(result)


# 初版不支持额外的透明信息和背景色
read_png = read_png2


def write_png(width, height, mode, data):
    if mode == 'light':
        color_type = COLOR_TYPE_GRAY
        row_bytes = width
    elif mode == 'rgb':
        color_type = COLOR_TYPE_RGB
        row_bytes = width * 3
    elif mode == 'alpha':
        color_type = COLOR_TYPE_RGB_ALPHA
        row_bytes = width * 4
    else:
        raise

    header_data = struct.pack('!2I5B', width, height, 8, color_type, 0, 0, 0)
    header_crc32 = struct.pack('!I', zlib.crc32(HEADER + header_data))

    def meow():
        iter_data = iter(data)
        for _ in range(height):
            yield 0
            for _ in range(row_bytes):
                yield next(iter_data)

    filtered_image = bytes(meow())
    zipped_image = zlib.compress(filtered_image)
    zipped_length = struct.pack('!I', len(zipped_image))
    zipped_crc32 = struct.pack('!I', zlib.crc32(DATA + zipped_image))

    result = io.BytesIO()
    result.write(b'\x89PNG\r\n\x1a\n')
    result.write(b'\x00\x00\x00\r\x49\x48\x44\x52')
    result.write(header_data)
    result.write(header_crc32)
    result.write(zipped_length)
    result.write(DATA)
    result.write(zipped_image)
    result.write(zipped_crc32)
    result.write(b'\x00\x00\x00\x00\x49\x45\x4e\x44\xaeB`\x82')

    return result.getvalue()


def write_png2(width, height, mode, data, data_split=40503):
    if mode == 'light':
        color_type = COLOR_TYPE_GRAY
        row_bytes = width
    elif mode == 'rgb':
        color_type = COLOR_TYPE_RGB
        row_bytes = width * 3
    elif mode == 'alpha':
        color_type = COLOR_TYPE_RGB_ALPHA
        row_bytes = width * 4
    else:
        raise

    header_data = struct.pack('!2I5B', width, height, 8, color_type, 0, 0, 0)
    header_crc32 = struct.pack('!I', zlib.crc32(HEADER + header_data))

    filtered_image = io.BytesIO()

    for i in range(0, len(data), row_bytes):
        filtered_image.write(b'\x00')
        filtered_image.write(data[i: i + row_bytes])

    zipped_data = zlib.compress(filtered_image.getvalue())
    split_data = (zipped_data[i: i + data_split]
                  for i in range(0, len(zipped_data), data_split))

    result = io.BytesIO()
    result.write(b'\x89PNG\r\n\x1a\n')
    result.write(b'\x00\x00\x00\r\x49\x48\x44\x52')
    result.write(header_data)
    result.write(header_crc32)

    for s_data in split_data:
        s_length = struct.pack('!I', len(s_data))
        s_crc32 = struct.pack('!I', zlib.crc32(DATA + s_data))

        result.write(s_length)
        result.write(DATA)
        result.write(s_data)
        result.write(s_crc32)

    result.write(b'\x00\x00\x00\x00\x49\x45\x4e\x44\xaeB`\x82')

    return result.getvalue()


# 初版不支持 256 * 256 以上的信息
write_png = write_png2


__all__ = ['read_png', 'write_png']

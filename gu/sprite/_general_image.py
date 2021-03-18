import io

from .png_library import read_png

from ..system import resource


class GeneralImage:
    """ 只支持 png 喔，如果有装 pillow 就可以把其它格式加进来了 """

    def __init__(self, image_route):
        _image_data = resource.get(image_route)

        if not _image_data:
            # 是否对包外的数据进行读取呢？
            raise FileNotFoundError

        try:
            _width, _height, _mode, _data = read_png(io.BytesIO(_image_data))

        except TypeError:
            try:
                import PIL.Image
                _im = PIL.Image.open(io.BytesIO(_image_data))
                _width, _height = _im.size
                _data = _im.tobytes()
                _pil_mode = _im.mode
                if _pil_mode == 'L':
                    _mode = 'gray'
                elif _pil_mode == 'RGB':
                    _mode = 'rgb'
                else:
                    _mode = 'full'

            except ImportError:
                raise NotImplementedError


import sys

if sys.platform in ('win32', 'cygwin'):
    platform = 0

    # keyboard
    # esc f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12
    # grave 1 2 3 4 5 6 7 8 9 0 -(minus) =(equal) delete
    # tab q w e r t y u i o p [(left_bracket) ](right_bracket) \(backslash)
    # caps a s d f g h j k l ;(semicolon) '(quote) enter
    # shift z x c v b n m ,(comma) .(period) /(slash) shift
    # ctrl alt space ctrl alt left up down right
    key_map = {}

elif sys.platform == 'darwin':
    platform = 1
    key_map = {  # 这里所有的按键实际上是 unsigned，但是在 python 里是 signed
        'Esc': 0x35, 'F1': 0x7A, 'F2': 0x78, 'F3': 0x63, 'F4': 0x76,
        'F5': 0x60, 'F6': 0x61, 'F7': 0x62, 'F8': 0x64,
        'F9': 0x65, 'F10 ': 0x6D, 'F11 ': 0x67, 'F12 ': 0x6F,

        'Grave': 0x32, '1': 0x12, '2': 0x13, '3': 0x14, '4': 0x15,
        '5': 0x17, '6': 0x16, '7': 0x1A, '8': 0x1C,
        '9': 0x19, '0': 0x1D, 'Minus': 0x1B, 'Equal': 0x18,

        'Tab': 0x30, 'Q': 0x0C, 'W': 0x0D, 'E': 0x0E, 'R': 0x0F,
        'T': 0x11, 'Y': 0x10, 'U': 0x20, 'I': 0x22, 'O': 0x1F, 'P': 0x23,
        'LeftBracket': 0x21, 'RightBracket': 0x1E, 'Backslash': 0x2A,

        'Caps': 0x39, 'A': 0x00, 'S': 0x01, 'D': 0x02, 'F': 0x03,  # 注意这里的 A
        'G': 0x05, 'H': 0x04, 'J': 0x26, 'K': 0x28,
        'L': 0x25, 'Semicolon': 0x29, 'Quote': 0x27, 'Enter': 0x24,

        'Shift': 0x38, 'Z': 0x06, 'X': 0x07, 'C': 0x08, 'V': 0x09,
        'B': 0x0B, 'N': 0x2D, 'M': 0x2E, 'Comma': 0x2B,
        'Period': 0x2F, 'Slash': 0x2C, 'RightShift': 0x3C,

        'Ctrl': 0x37, 'Alt': 0x3A, 'Space': 0x31, 'RightCtrl': 0x36,
        'RightAlt': 0x3D, 'Left ': 0x7B, 'Up': 0x7E,
        'Down ': 0x7D, 'Right': 0x7C
    }

else:
    platform = 2
    key_map = {}


def do_nothing(*args, **kwargs):
    print(args, kwargs)


_FLAG_SIGN_BIT = 0x400, 0x200, 0x100
_FLAG_MAP_CODE = (  # _FLAG_CODES.index(key) // 2
    key_map['Ctrl'], key_map['RightCtrl'],
    key_map['Alt'], key_map['RightAlt'],
    key_map['Shift'], key_map['RightShift']
)
_NULL_KEY = -1


class Keyboard(object):
    def __init__(self):
        self._keyboard_press_function = {}
        self._keyboard_release_function = {}
        self._keyboard_last_key = _NULL_KEY  # 如果有最后一个 key 表示是持续按压
        self._keyboard_hold_function = {}
        self._keyboard_hold_count = 0  # 用于记录 hold 函数的次数
        self._keyboard_flag = 0  # 快捷键按钮检测

    def __getattr__(self, item):
        underscore_split = item.split('_')
        mode = underscore_split[0]  # 第一个文本为状态说明

        if 'Press' == mode:
            mode = self._keyboard_press_function
        elif 'Hold' == mode:
            mode = self._keyboard_hold_function
        elif 'Release' == mode:
            mode = self._keyboard_release_function
        else:
            raise ValueError('Press Hold Release')

        key = key_map.get(underscore_split[-1], None)  # 最后一个文本为按键
        if key is None:
            return

        flags = underscore_split[1: -1]
        if 'Ctrl' in flags:
            key |= _FLAG_SIGN_BIT[0]
        if 'Alt' in flags:
            key |= _FLAG_SIGN_BIT[1]
        if 'Shift' in flags:
            key |= _FLAG_SIGN_BIT[2]

        def wrap_function(function):
            mode[key] = function
            return function

        return wrap_function

    def __call__(self, key=None, hold=False):
        if hold:  # 如果和鼠标混合点击，会导致这里按键持续
            if self._keyboard_last_key != _NULL_KEY:
                self._keyboard_hold_count += 1
                self._keyboard_hold_function.get(
                    self._keyboard_last_key, do_nothing
                )(self._keyboard_hold_count)

        elif key in _FLAG_MAP_CODE:  # 表示这是快捷键
            flag = _FLAG_SIGN_BIT[_FLAG_MAP_CODE.index(key) // 2]
            if self._keyboard_flag & flag:
                self._keyboard_flag &= ~flag
            else:
                self._keyboard_flag |= flag

        else:
            key |= self._keyboard_flag

            if self._keyboard_last_key != _NULL_KEY:
                self._keyboard_hold_count = 0
                self._keyboard_last_key = _NULL_KEY
                self._keyboard_release_function.get(key, do_nothing)()
            else:
                self._keyboard_last_key = key
                self._keyboard_press_function.get(key, do_nothing)()

    def user_set(self, user_dict):
        """
        从用户载入键盘设置
        """
        raise NotImplementedError


class Gu(dict):
    platform = platform
    keyboard = Keyboard()

    def __init__(self):
        dict.__init__(self)
        self.__dict__ = self

    @staticmethod
    def bind_dynamic_library(lib, fallback=None):
        """
        绑定函数

        输入已加载的动态库，返回绑定用函数
        """

        def _bind(name, restype, *arg_types):
            """
            从动态库里绑定函数的函数
            """
            try:
                _func = getattr(lib, name)
                _func.restype = restype
                setattr(_func, 'arg''types', arg_types)

            except AttributeError:  # 绑定失败，返回无效函数
                if fallback:
                    _func = fallback(name, restype, *arg_types)
                else:
                    def _func(*args):  # 无法加载的函数，默认使用这个
                        print('<Error Func>', lib, name, args)

            return _func

        return _bind


gu = Gu()

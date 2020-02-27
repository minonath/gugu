import ctypes
import typing
import math


_c_type = type(ctypes.c_ubyte)


class Array(object):
    __length__ = 1

    def __init__(self, *args, length=0, _type=ctypes.c_float):
        if not length:
            length = self.__length__

        self.__values__ = (_type * length)(*args)
        self.__length__ = length
        self.__e_size__ = ctypes.sizeof(_type)
        self.__b_size__ = length * self.__e_size__
        self.__e_type__ = _type
        self.__string__ = self.__class__.__name__ + '(%s)' % ', '.join(
            '{:.3f}' for _ in range(length))

    @property
    def _as_parameter_(self):
        return self.__values__

    def __getitem__(self, item):
        return self.__values__[item]

    def __setitem__(self, key, value):
        self.__values__[key] = value

    def __repr__(self):
        return self.__string__.format(*self)

    def __call__(self, *args):
        self.__values__[:] = args
        return self

    @property
    def array_length(self) -> int:
        return self.__length__

    @property
    def array_size(self) -> int:
        return self.__b_size__

    @property
    def array_element_type(self) -> _c_type:
        return self.__e_type__

    @property
    def array_element_size(self) -> int:
        return self.__e_size__


class Matrix4(Array):
    __length__ = 16

    def matrix_from_inverse(self, other):
        pass

    @staticmethod
    def matrix_perspective(
            fov=75.0, aspect=16 / 9, near=0.1, far=1000.0):
        _semi_y = near * math.tan(math.radians(fov / 2))
        _semi_x = _semi_y * aspect
        _width = _semi_x + _semi_x
        _height = _semi_y + _semi_y
        _depth = far - near
        print(_semi_x, _semi_y)
        # [2] = (_semi_x + -_semi_x) / _width
        # [6] = (_semi_y + -_semi_y) / _height
        return (
            2.0 * near / _width, 0.0, 0.0, 0.0,
            0.0, 2.0 * near / _height, 0.0, 0.0,
            0.0, 0.0, -(far + near) / _depth, -1.0,
            0.0, 0.0, -2.0 * far * near / _depth, 0.0
        )

    @staticmethod
    def matrix_look_at(eye, target, up):
        _ex, _ey, _ez = eye
        _tx, _ty, _tz = target

        # target - eye
        _toward = array_normalize((_tx - _ex, _ty - _ey, _tz - _ez))
        # cross(_toward, up)
        _side = array_normalize(vector3_cross(_toward, up))
        # cross(_toward, up)
        _up = array_normalize(vector3_cross(_side, _toward))

        return (
            _side[0], _up[0], -_toward[0], 0.0,
            _side[1], _up[1], -_toward[1], 0.0,
            _side[2], _up[2], -_toward[2], 0.0,
            -vector3_dot(_side, eye), -vector3_dot(_up, eye),
            vector3_dot(_toward, eye), 1.0
        )

    @staticmethod
    def matrix_multiply(self, other):
        (s11, s21, s31, s41, s12, s22, s32, s42,
         s13, s23, s33, s43, s14, s24, s34, s44) = self
        (m11, m21, m31, m41, m12, m22, m32, m42,
         m13, m23, m33, m43, m14, m24, m34, m44) = other

        return (
            s11 * m11 + s12 * m21 + s13 * m31 + s14 * m41,
            s21 * m11 + s22 * m21 + s23 * m31 + s24 * m41,
            s31 * m11 + s32 * m21 + s33 * m31 + s34 * m41,
            s41 * m11 + s42 * m21 + s43 * m31 + s44 * m41,
            s11 * m12 + s12 * m22 + s13 * m32 + s14 * m42,
            s21 * m12 + s22 * m22 + s23 * m32 + s24 * m42,
            s31 * m12 + s32 * m22 + s33 * m32 + s34 * m42,
            s41 * m12 + s42 * m22 + s43 * m32 + s44 * m42,
            s11 * m13 + s12 * m23 + s13 * m33 + s14 * m43,
            s21 * m13 + s22 * m23 + s23 * m33 + s24 * m43,
            s31 * m13 + s32 * m23 + s33 * m33 + s34 * m43,
            s41 * m13 + s42 * m23 + s43 * m33 + s44 * m43,
            s11 * m14 + s12 * m24 + s13 * m34 + s14 * m44,
            s21 * m14 + s22 * m24 + s23 * m34 + s24 * m44,
            s31 * m14 + s32 * m24 + s33 * m34 + s34 * m44,
            s41 * m14 + s42 * m24 + s43 * m34 + s44 * m44
        )

    @staticmethod
    def matrix_rotation_z(theta):
        theta = math.radians(theta)
        c = math.cos(theta)
        s = math.sin(theta)

        return (c, - s, 0.0, 0.0,
                s, c, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
                )

    @staticmethod
    def matrix_rotation_y(theta):
        theta = math.radians(theta)
        c = math.cos(theta)
        s = math.sin(theta)

        return (c, 0.0, s, 0.0,
                0.0, 1.0, 0.0, 0.0,
                -s, 0.0, c, 0.0,
                0.0, 0.0, 0.0, 1.0)


class Quaternion(Array):
    __length__ = 4


class Vector3(Array):
    __length__ = 3


def vector3_cross(vector3_a, vector3_b):
    ax, ay, az = vector3_a
    bx, by, bz = vector3_b
    return ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx


def vector3_dot(vector3_a, vector3_b):
    ax, ay, az = vector3_a
    bx, by, bz = vector3_b
    return ax * bx + ay * by + az * bz


def array_normalize(array_type):
    _length = sum(_i * _i for _i in array_type) ** 0.5
    if _length:
        return tuple(_i / _length for _i in array_type)

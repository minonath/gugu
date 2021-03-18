import math

from ._array import *


class Vector3(Floats):
    def __sub__(self, other):
        return self.__class__(
            self[0] - other[0], self[1] - other[1], self[2] - other[2]
        )

    def normalize(self):
        k = sum(i * i for i in self) ** 0.5
        if k:
            return self.__class__(self[0] / k, self[1] / k, self[2] / k)
        else:
            return self.__class__(*self)

    def __and__(self, other):  # 用 & 表示点乘 dot
        return sum(x * y for x, y in zip(self, other))

    def __or__(self, other):  # 用 | 表示叉乘 cross
        sx, sy, sz = self
        ox, oy, oz = other

        return self.__class__(
            sy * oz - sz * oy, sz * ox - sx * oz, sx * oy - sy * ox
        )


class Matrix4(Floats):
    @classmethod
    def from_look_at(cls, eye, target, up):
        a = (target - eye).normalize()
        b = (a | up).normalize()
        c = (b | a).normalize()

        return cls(b[0], c[0], -a[0], 0, b[1], c[1], -a[1], 0,
                   b[2], c[2], -a[2], 0, -(b & eye), -(c & eye), a & eye, 1)

    @classmethod
    def matrix4_from_perspective_bounds(
            cls, left, right, bottom, top, near, far):
        _x = 2 * near / (right - left)
        _y = 2 * near / (top - bottom)
        _a = (right + left) / (right - left)
        _b = (top + bottom) / (top - bottom)
        _c = - (far + near) / (far - near)
        _d = - 2 * far * near / (far - near)
        return cls(_x, 0, 0, 0, 0, _y, 0, 0, _a, _b, _c, -1, 0, 0, _d, 0)

    @classmethod
    def from_perspective(cls, fov, aspect, near, far):
        _semi_y = near * math.tan(math.radians(fov / 2))
        _semi_x = _semi_y * aspect
        return cls.matrix4_from_perspective_bounds(
            -_semi_x, _semi_x, -_semi_y, _semi_y, near, far)

    def __mul__(self, other):
        (_m11, _m21, _m31, _m41, _m12, _m22, _m32, _m42,
         _m13, _m23, _m33, _m43, _m14, _m24, _m34, _m44) = self
        (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
         _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = other

        return self.__class__(
            _m11 * _n11 + _m12 * _n21 + _m13 * _n31 + _m14 * _n41,
            _m21 * _n11 + _m22 * _n21 + _m23 * _n31 + _m24 * _n41,
            _m31 * _n11 + _m32 * _n21 + _m33 * _n31 + _m34 * _n41,
            _m41 * _n11 + _m42 * _n21 + _m43 * _n31 + _m44 * _n41,
            _m11 * _n12 + _m12 * _n22 + _m13 * _n32 + _m14 * _n42,
            _m21 * _n12 + _m22 * _n22 + _m23 * _n32 + _m24 * _n42,
            _m31 * _n12 + _m32 * _n22 + _m33 * _n32 + _m34 * _n42,
            _m41 * _n12 + _m42 * _n22 + _m43 * _n32 + _m44 * _n42,
            _m11 * _n13 + _m12 * _n23 + _m13 * _n33 + _m14 * _n43,
            _m21 * _n13 + _m22 * _n23 + _m23 * _n33 + _m24 * _n43,
            _m31 * _n13 + _m32 * _n23 + _m33 * _n33 + _m34 * _n43,
            _m41 * _n13 + _m42 * _n23 + _m43 * _n33 + _m44 * _n43,
            _m11 * _n14 + _m12 * _n24 + _m13 * _n34 + _m14 * _n44,
            _m21 * _n14 + _m22 * _n24 + _m23 * _n34 + _m24 * _n44,
            _m31 * _n14 + _m32 * _n24 + _m33 * _n34 + _m34 * _n44,
            _m41 * _n14 + _m42 * _n24 + _m43 * _n34 + _m44 * _n44
        )

import math

from gu.system.other import Array


def matrix4_from_perspective_bounds(
        left, right, bottom, top, near, far, result):
    # 注意输入顺序，左右上下近远
    _x = 2 * near / (right - left)
    _y = 2 * near / (top - bottom)
    _a = (right + left) / (right - left)
    _b = (top + bottom) / (top - bottom)
    _c = - (far + near) / (far - near)
    _d = - 2 * far * near / (far - near)
    result(_x, 0, 0, 0, 0, _y, 0, 0, _a, _b, _c, -1, 0, 0, _d, 0)


def vector3_length(self):
    return sum(_x ** 2 for _x in self) ** 0.5


def vector3_dot_vector3(self, other):
    return sum(_x * _y for _x, _y in zip(self, other))


def vector3_sub_vector3(self, other, result):
    result(*(_x - _y for _x, _y in zip(self, other)))


def vector3_normalize(self, result):
    _length = vector3_length(self)
    if _length:
        result(*(_x / _length for _x in self))


def vector3_cross_vector3(self, other, result):
    _sx, _sy, _sz = self
    _ox, _oy, _oz = other

    result(
        _sy * _oz - _sz * _oy, _sz * _ox - _sx * _oz, _sx * _oy - _sy * _ox)


vector3_0 = Array(element_nums=3)
vector3_1 = Array(element_nums=3)
vector3_2 = Array(element_nums=3)


def matrix4_from_look_at(eye, target, up, result):
    vector3_sub_vector3(target, eye, vector3_2)
    vector3_normalize(vector3_2, vector3_2)
    vector3_cross_vector3(vector3_2, up, vector3_0)
    vector3_normalize(vector3_0, vector3_0)
    vector3_cross_vector3(vector3_0, vector3_2, vector3_1)
    vector3_normalize(vector3_1, vector3_1)
    return result(vector3_0[0], vector3_1[0], -vector3_2[0], 0,
                  vector3_0[1], vector3_1[1], -vector3_2[1], 0,
                  vector3_0[2], vector3_1[2], -vector3_2[2], 0,
                  -vector3_dot_vector3(vector3_0, eye),
                  -vector3_dot_vector3(vector3_1, eye),
                  vector3_dot_vector3(vector3_2, eye), 1)


class Matrix4(Array):
    _array_element_nums = 16


class Vector3(Array):
    _array_element_nums = 3


def from_look_at(eye, target, up):
    result = Matrix4()
    matrix4_from_look_at(eye, target, up, result)
    return result


def from_perspective_bounds(left, right, bottom, top, near, far):
    result = Matrix4()
    matrix4_from_perspective_bounds(
        left, right, bottom, top, near, far, result)
    return result


def from_perspective(fov, aspect, near, far):
    result = Matrix4()
    _semi_y = near * math.tan(math.radians(fov / 2))
    _semi_x = _semi_y * aspect
    matrix4_from_perspective_bounds(-_semi_x, _semi_x, -_semi_y,
                                    _semi_y, near, far, result)
    return result


def matrix4_mul_matrix4(self, other, result):
    (_m11, _m21, _m31, _m41, _m12, _m22, _m32, _m42,
     _m13, _m23, _m33, _m43, _m14, _m24, _m34, _m44) = self
    (_n11, _n21, _n31, _n41, _n12, _n22, _n32, _n42,
     _n13, _n23, _n33, _n43, _n14, _n24, _n34, _n44) = other

    result(
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


def project_matrix(fov, aspect, near, far):
    return from_perspective(fov, aspect, near, far)


def camera_matrix(e0, e1, e2, t0, t1, t2, u0, u1, u2):
    return from_look_at(
        Vector3(e0, e1, e2), Vector3(t0, t1, t2), Vector3(u0, u1, u2))


# def
#     c = Matrix4()
#     matrix4_mul_matrix4(a, b, c)
#     return a, b, c

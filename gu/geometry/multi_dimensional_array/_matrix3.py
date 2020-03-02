# include "_array.py" /*

import math
from ._array import ctypes_wrap, VOIDP, FLT


@ctypes_wrap(None, VOIDP)
def matrix3_from_identity(result):
    """ */

    static float matrix3_identity[9] = {
        1.0f, 0.0f, 0.0f,
        0.0f, 1.0f, 0.0f,
        0.0f, 0.0f, 1.0f
    };

    void matrix3_from_identity(float *result) {
        memcpy(result, matrix3_identity, 9 * sizeof(float));
    }
    /* """
    result(1, 0, 0, 0, 1, 0, 0, 0, 1)


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix3_from_matrix4(matrix4, result):
    """ */

    void matrix3_from_matrix4(const float *matrix4, float *result) {
        memcpy(result, matrix4, 3 * sizeof(float));
        memcpy(result + 3, matrix4 + 4, 3 * sizeof(float));
        memcpy(result + 6, matrix4 + 8, 3 * sizeof(float));
    }
    /* """
    (_m11, _m21, _m31, _, _m12, _m22, _m32, _,
     _m13, _m23, _m33, _, _, _, _, _) = matrix4
    result(_m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33)


@ctypes_wrap(None, VOIDP, VOIDP, VOIDP)
def matrix3_mul_matrix3(self, other, result):
    """ */

    void matrix3_mul_matrix3(const float *self, const float *other,
                             float *result) {
        float cache[9] = {
            self[0] * other[0] + self[3] * other[1] + self[6] * other[2],
            self[1] * other[0] + self[4] * other[1] + self[7] * other[2],
            self[2] * other[0] + self[5] * other[1] + self[8] * other[2],
            self[0] * other[3] + self[3] * other[4] + self[6] * other[5],
            self[1] * other[3] + self[4] * other[4] + self[7] * other[5],
            self[2] * other[3] + self[5] * other[4] + self[8] * other[5],
            self[0] * other[6] + self[3] * other[7] + self[6] * other[8],
            self[1] * other[6] + self[4] * other[7] + self[7] * other[8],
            self[2] * other[6] + self[5] * other[7] + self[8] * other[8]
        };
        memcpy(result, cache, 9 * sizeof(float));
    }
    /* """
    _a11, _a21, _a31, _a12, _a22, _a32, _a13, _a23, _a33 = self
    _b11, _b21, _b31, _b12, _b22, _b32, _b13, _b23, _b33 = other

    result(
        _a11 * _b11 + _a12 * _b21 + _a13 * _b31,
        _a21 * _b11 + _a22 * _b21 + _a23 * _b31,
        _a31 * _b11 + _a32 * _b21 + _a33 * _b31,
        _a11 * _b12 + _a12 * _b22 + _a13 * _b32,
        _a21 * _b12 + _a22 * _b22 + _a23 * _b32,
        _a31 * _b12 + _a32 * _b22 + _a33 * _b32,
        _a11 * _b13 + _a12 * _b23 + _a13 * _b33,
        _a21 * _b13 + _a22 * _b23 + _a23 * _b33,
        _a31 * _b13 + _a32 * _b23 + _a33 * _b33
    )


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def matrix3_mul_scalar(self, other, result):
    """ */

    void matrix3_mul_scalar(const float *self, float other, float *result) {
        for (int i = 0; i < 9; i ++) result[i] = self[i] * other;
    }
    /* """
    result(*(_x * other for _x in self))


@ctypes_wrap(None, VOIDP)
def matrix3_determinant(self):
    """ */

    float matrix3_determinant(const float *self) {
        return self[0] * self[4] * self[8] - self[0] * self[5] * self[7] -
               self[1] * self[3] * self[8] + self[1] * self[5] * self[6] +
               self[2] * self[3] * self[7] - self[2] * self[4] * self[6];
    }
    /* """
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = self
    return (_m11 * _m22 * _m33 - _m11 * _m32 * _m23 - _m21 * _m12 * _m33 +
            _m21 * _m32 * _m13 + _m31 * _m12 * _m23 - _m31 * _m22 * _m13)


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix3_inverse(self, result):
    """ */

    void matrix3_inverse(const float *self, float *result) {
        float cache[9] = {
            self[8] * self[4] - self[5] * self[7],
            self[2] * self[7] - self[8] * self[1],
            self[5] * self[1] - self[2] * self[4],
            self[5] * self[6] - self[8] * self[3],
            self[8] * self[0] - self[2] * self[6],
            self[2] * self[3] - self[5] * self[0],
            self[7] * self[3] - self[4] * self[6],
            self[1] * self[6] - self[7] * self[0],
            self[4] * self[0] - self[1] * self[3]
        };
        float det =
            self[0] * cache[0] + self[1] * cache[3] + self[2] * cache[6];
        if (det == 0.0f) memcpy(result, matrix3_identity, 9 * sizeof(float));
        else for (int i = 0; i < 9; i ++) result[i] = cache[i] / det;
    }
    /* """
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = self
    _t11 = _m33 * _m22 - _m32 * _m23
    _t12 = _m32 * _m13 - _m33 * _m12
    _t13 = _m23 * _m12 - _m22 * _m13
    _det = _m11 * _t11 + _m21 * _t12 + _m31 * _t13  # determinant
    if _det:
        _det = 1 / _det
        result(
            _t11 * _det, (_m31 * _m23 - _m33 * _m21) * _det,
            (_m32 * _m21 - _m31 * _m22) * _det,
            _t12 * _det, (_m33 * _m11 - _m31 * _m13) * _det,
            (_m31 * _m12 - _m32 * _m11) * _det,
            _t13 * _det, (_m21 * _m13 - _m23 * _m11) * _det,
            (_m22 * _m11 - _m21 * _m12) * _det
        )
    else:
        matrix3_from_identity(result)


@ctypes_wrap(None, VOIDP, VOIDP)
def matrix3_transpose(self, result):
    """ */

    void matrix3_transpose(const float *self, float *result) {
        float tmp;  // 使用临时变量进行交换，swap。
        tmp = self[3]; result[3] = self[1]; result[1] = tmp;
        tmp = self[6]; result[6] = self[2]; result[2] = tmp;
        tmp = self[7]; result[7] = self[5]; result[5] = tmp;
        result[0] = self[0];
        result[4] = self[4];
        result[8] = self[8];
    }
    /* """
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = self
    result(_m11, _m12, _m13, _m21, _m22, _m23, _m31, _m32, _m33)


@ctypes_wrap(None, FLT, FLT, FLT, FLT, FLT, FLT, FLT, VOIDP)
def matrix3_from_uv_transform(tx, ty, sx, sy, rotation, cx, cy, result):
    """ */

    void matrix3_from_uv_transform(float tx, float ty, float sx, float sy,
                                   float rotation, float cx, float cy,
                                   float *result) {
        float _c = cosf(rotation), _s = sinf(rotation);
        result[0] = sx * _c; result[1] = sx * _s;
        result[2] = - sx * (_c * cx + _s * cy) + cx + tx;
        result[3] = - sy * _s; result[4] = sy * _c;
        result[5] = - sy * (- _s * cx + _c * cy) + cy + ty;
        result[6] =  result[7] = 0.0f; result[8] = 1.0f;
    }
    /* """
    _c = math.cos(rotation)
    _s = math.sin(rotation)
    result(
        sx * _c, sx * _s, - sx * (_c * cx + _s * cy) + cx + tx, - sy * _s,
        sy * _c, - sy * (- _s * cx + _c * cy) + cy + ty, 0, 0, 1
    )


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def matrix3_scale(self, sx, sy, result):
    """ */

    void matrix3_scale(const float *self, float sx, float sy, float *result) {
        result[0] = self[0] * sx;
        result[1] = self[1] * sy; result[2] = self[2];
        result[3] = self[3] * sx;
        result[4] = self[4] * sy; result[5] = self[5];
        result[6] = self[6] * sx;
        result[7] = self[7] * sy; result[8] = self[8];
    }
    /* """
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = self
    result(_m11 * sx, _m21 * sy, _m31, _m12 * sx, _m22 * sy, _m32,
           _m13 * sx, _m23 * sy, _m33)


@ctypes_wrap(None, VOIDP, FLT, VOIDP)
def matrix3_rotate(self, theta, result):
    """ */

    void matrix3_rotate(const float *self, float theta, float *result) {
        float c = cosf(theta), s = sinf(theta), m, n;
        m = c * self[0] + s * self[1]; n = - s * self[0] + c * self[1];
        result[0] = m; result[1] = n; result[2] = self[2];
        m = c * self[3] + s * self[4]; n = - s * self[3] + c * self[4];
        result[3] = m; result[4] = n; result[5] = self[5];
        m = c * self[6] + s * self[7]; n = - s * self[6] + c * self[7];
        result[6] = m; result[7] = n; result[8] = self[8];
    }
    /* """
    _c = math.cos(theta)
    _s = math.sin(theta)
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = self

    result(
        _c * _m11 + _s * _m21, - _s * _m11 + _c * _m21, _m31,
        _c * _m12 + _s * _m22, - _s * _m12 + _c * _m22, _m32,
        _c * _m13 + _s * _m23, - _s * _m13 + _c * _m23, _m33
    )


@ctypes_wrap(None, VOIDP, FLT, FLT, VOIDP)
def matrix3_translate(self, tx, ty, result):
    """ */

    void matrix3_translate(const float *self, float tx, float ty,
                           float *result) {
        result[0] = self[0] + tx * self[2];  // 顺序计算，结果不会受到计算影响
        result[1] = self[1] + ty * self[2]; result[2] = self[2];
        result[3] = self[3] + tx * self[5];
        result[4] = self[4] + ty * self[5]; result[5] = self[5];
        result[6] = self[6] + tx * self[8];
        result[7] = self[7] + ty * self[8]; result[8] = self[8];
    }
    /* """
    _m11, _m21, _m31, _m12, _m22, _m32, _m13, _m23, _m33 = self

    return (result or self)(
        _m11 + tx * _m31, _m21 + ty * _m31, _m31,
        _m12 + tx * _m32, _m22 + ty * _m32, _m32,
        _m13 + tx * _m33, _m23 + ty * _m33, _m33)

# */

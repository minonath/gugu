from ._matrix3 import *
from ._matrix4 import *
from ._quaternion import *
from ._vector2 import *
from ._vector3 import *
from ._vector4 import *
from .. import Array, Matrix3, Matrix4, Quaternion, Euler, \
    Vector2, Vector3, Vector4


def equals(self, other):
    # 这里返回误差值，具体是否相等自己看
    return max(abs(x - y) for x, y in zip(self, other))


def equals2(self, other):
    # Quaternion 正反相同
    a = max(abs(x - y) for x, y in zip(self, other))
    b = max(abs(x + y) for x, y in zip(self, other))
    return min(a, b)

# 从这里导出的函数一定是 python 写的


Array.__eq__ = equals
Matrix3.__eq__ = equals
Matrix4.__eq__ = equals
Quaternion.__eq__ = equals2
Euler.__eq__ = equals
Vector2.__eq__ = equals
Vector3.__eq__ = equals
Vector4.__eq__ = equals

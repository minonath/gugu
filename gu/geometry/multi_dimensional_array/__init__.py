import math
from .makefile import *

from ._array import Array, non_zero, clamp, xyz, yxz, zxy, zyx, yzx, xzy, \
    float_nan, float_inf, float_max, float_min, quaternion_0, matrix4_0


class Vector2(Array):
    __length__ = 2

    def __add__(self, other):
        result = Vector2()
        if isinstance(other, (float, int)):
            vector2_add_scalar(self, other, result)
        elif isinstance(other, Vector2):
            vector2_add_vector2(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __radd__(self, other):
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_add_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_sub_scalar(self, other, result)
        elif isinstance(other, Vector2):
            vector2_sub_vector2(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rsub__(self, other):  # 等于加上相反数，再使用加法交换律
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_negate(self, result)
            vector2_add_scalar(result, other, result)
        else:
            raise NotImplementedError

        return result

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_mul_scalar(self, other, result)
        elif isinstance(other, Vector2):
            vector2_mul_vector2(self, other, result)
        elif isinstance(other, Matrix3):
            vector2_mul_matrix3(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rmul__(self, other):
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_mul_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_div_scalar(self, other, result)
        elif isinstance(other, Vector2):
            vector2_div_vector2(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rtruediv__(self, other):
        result = Vector2()

        if isinstance(other, (float, int)):
            vector2_div_vector2(Vector2(other, other), self, result)
        else:
            raise NotImplementedError

        return result

    def __itruediv__(self, other):
        return self.__truediv__(other)

    @staticmethod
    def min(self, other):
        result = Vector2()
        vector2_min_vector2(self, other, result)
        return result

    @staticmethod
    def max(self, other):
        result = Vector2()
        vector2_max_vector2(self, other, result)
        return result

    def clamp(self, other_min, other_max):
        result = Vector2()

        if isinstance(other_min, Vector2):  # and other_max
            vector2_clamp_vector2(self, other_min, other_max, result)
        elif isinstance(other_min, (float, int)):  # and other_max
            vector2_clamp_scalar(self, other_min, other_max, result)
        else:
            raise NotImplementedError

        return result

    def clamp_length(self, other_min, other_max):
        result = Vector2()
        vector2_clamp_length(self, other_min, other_max, result)
        return result

    def __floor__(self):
        result = Vector2()
        vector2_floor(self, result)
        return result

    def __ceil__(self):
        result = Vector2()
        vector2_ceil(self, result)
        return result

    def __round__(self):
        result = Vector2()
        vector2_round(self, result)
        return result

    def __trunc__(self):
        result = Vector2()
        vector2_trunc(self, result)
        return result

    def __neg__(self):
        result = Vector2()
        vector2_negate(self, result)
        return result

    def __and__(self, other):  # 用 & 表示点乘 dot
        return vector2_dot_vector2(self, other)

    def __or__(self, other):  # 用 | 表示叉乘 cross
        return vector2_cross_vector2(self, other)

    @property
    def length(self):
        return vector2_length(self)

    @length.setter
    def length(self, value):
        _origin = vector2_length(self)
        if _origin:
            vector2_mul_scalar(self, value / _origin, self)

    @property
    def length_squared(self):
        return vector2_length_squared(self)

    @property
    def length_manhattan(self):
        return vector2_length_manhattan(self)

    def normalize(self):
        result = Vector2()
        vector2_normalize(self, result)
        return result

    @property
    def angle(self):
        return vector2_angle(self)

    def rotate_around(self, other, angle):  # 逆时针转圈
        result = Vector2()
        vector2_rotate_around(self, other, angle, result)
        return result


def distance(a, b):
    if isinstance(a, Vector2):
        return vector2_distance_to_vector2(a, b)
    elif isinstance(a, Vector3):
        return vector3_distance_to_vector3(a, b)
    else:
        raise NotImplementedError


def distance_squared(a, b):
    if isinstance(a, Vector2):
        return vector2_distance_squared_to_vector2(a, b)
    elif isinstance(a, Vector3):
        return vector3_distance_squared_to_vector3(a, b)
    else:
        raise NotImplementedError


def distance_manhattan(a, b):
    if isinstance(a, Vector2):
        return vector2_distance_manhattan_to_vector2(a, b)
    elif isinstance(a, Vector3):
        return vector3_distance_manhattan_to_vector3(a, b)
    else:
        raise NotImplementedError


def interpolation(self, other, alpha):
    if isinstance(self, Vector2):
        result = Vector2()
        vector2_interpolation(self, other, alpha, result)
    elif isinstance(self, Vector3):
        result = Vector3()
        vector3_interpolation(self, other, alpha, result)
    elif isinstance(self, Vector4):
        result = Vector4()
        vector4_interpolation(self, other, alpha, result)
    elif isinstance(self, Quaternion):
        result = Quaternion()
        quaternion_spherical_linear_interpolation(self, other, alpha, result)
    else:
        raise NotImplementedError

    return result


class Vector3(Array):
    __length__ = 3

    def __add__(self, other):
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_add_scalar(self, other, result)
        elif isinstance(other, Vector3):
            vector3_add_vector3(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __radd__(self, other):
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_add_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_sub_scalar(self, other, result)
        elif isinstance(other, Vector3):
            vector3_sub_vector3(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rsub__(self, other):  # 等于加上相反数，再使用加法交换律
        result = Vector3()
        if isinstance(other, (float, int)):
            vector3_negate(self, result)
            vector3_add_scalar(result, other, result)
        else:
            raise NotImplementedError

        return result

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_mul_scalar(self, other, result)
        elif isinstance(other, Vector3):
            vector3_mul_vector3(self, other, result)
        elif isinstance(other, Euler):
            quaternion_from_euler(other, other.order, quaternion_0)
            vector3_mul_quaternion(self, quaternion_0, result)
        elif isinstance(other, Vector4):  # AxisAngle
            quaternion_from_axis_angle(other, quaternion_0)
            vector3_mul_quaternion(self, quaternion_0, result)
        elif isinstance(other, Matrix3):
            vector3_mul_matrix3(self, other, result)
        elif isinstance(other, Matrix4):
            vector3_mul_matrix4(self, other, result)
        elif isinstance(other, Quaternion):
            vector3_mul_quaternion(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rmul__(self, other):
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_mul_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_div_scalar(self, other, result)
        elif isinstance(other, Vector3):
            vector3_div_vector3(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rtruediv__(self, other):  # 如果是矩阵的话，就会用 inverse 了
        result = Vector3()

        if isinstance(other, (float, int)):
            vector3_div_vector3(Vector3(other, other, other), self, result)
        else:
            raise NotImplementedError

        return result

    def __itruediv__(self, other):
        return self.__truediv__(other)

    @staticmethod
    def min(self, other):
        result = Vector3()
        vector3_min_vector3(self, other, result)
        return result

    @staticmethod
    def max(self, other):
        result = Vector3()
        vector3_max_vector3(self, other, result)
        return result

    def clamp(self, other_min, other_max):
        result = Vector3()

        if isinstance(other_min, Vector3):  # and other_max
            vector3_clamp_vector3(self, other_min, other_max, result)
        elif isinstance(other_min, (float, int)):  # and other_max
            vector3_clamp_scalar(self, other_min, other_max, result)
        else:
            raise NotImplementedError

        return result

    def clamp_length(self, other_min, other_max):
        result = Vector3()
        vector3_clamp_length(self, other_min, other_max, result)
        return result

    def __floor__(self):
        result = Vector3()
        vector3_floor(self, result)
        return result

    def __ceil__(self):
        result = Vector3()
        vector3_ceil(self, result)
        return result

    def __round__(self):
        result = Vector3()
        vector3_round(self, result)
        return result

    def __trunc__(self):
        result = Vector3()
        vector3_trunc(self, result)
        return result

    def __neg__(self):
        result = Vector3()
        vector3_negate(self, result)
        return result

    def __and__(self, other):  # 用 & 表示点乘 dot
        return vector3_dot_vector3(self, other)

    def __or__(self, other):  # 用 | 表示叉乘 cross
        result = Vector3()
        vector3_cross_vector3(self, other, result)
        return result

    @property
    def length(self):
        return vector3_length(self)

    @length.setter
    def length(self, value):
        _origin = vector3_length(self)
        if _origin:
            vector3_mul_scalar(self, value / _origin, self)

    @property
    def length_squared(self):
        return vector3_length_squared(self)

    @property
    def length_manhattan(self):
        return vector3_length_manhattan(self)

    def normalize(self):
        result = Vector3()
        vector3_normalize(self, result)
        return result

    def project(self, world_inverse, projection_matrix):
        result = Vector3()
        vector3_mul_matrix4(self, world_inverse, result)
        vector3_mul_matrix4(result, projection_matrix, result)
        return result

    def un_project(self, world_matrix, projection_inverse):
        result = Vector3()
        vector3_mul_matrix4(self, projection_inverse, result)
        vector3_mul_matrix4(result, world_matrix, result)
        return result

    def transform_direction(self, matrix4):
        result = Vector3()
        vector3_transform_direction(self, matrix4, result)
        return result

    def project_on_vector3(self, other):
        result = Vector3()
        vector3_project_vector3(self, other, result)
        return result

    def project_on_plane(self, normal):
        result = Vector3()
        vector3_project_vector3(self, normal, result)
        vector3_sub_vector3(self, result, result)
        return result

    def reflect(self, normal):
        result = Vector3()
        vector3_reflect(self, normal, result)
        return result

    def angle(self, other):
        return vector3_angle_to_vector3(self, other)

    @staticmethod
    def from_spherical(radius, phi, theta):
        result = Vector3()
        vector3_from_spherical(radius, phi, theta, result)
        return result

    @staticmethod
    def from_cylindrical(radius, theta, y):
        result = Vector3()
        vector3_from_cylindrical(radius, theta, y, result)
        return result

    @staticmethod
    def from_matrix4_offset(matrix4, offset=12):
        result = Vector3()
        vector3_from_matrix4_offset(matrix4, offset, result)
        return result

    @staticmethod
    def from_matrix4_scale(matrix4):
        result = Vector3()
        vector3_from_matrix4_scale(matrix4, result)
        return result


class Euler(Array):
    __length__ = 3

    def __init__(self, *args, order=xyz):
        Array.__init__(self, *args)
        if order in (xyz, yxz, zxy, zyx, yzx, xzy):
            self.order = order
        else:
            self.order = xyz

    def __repr__(self):
        return 'Euler({:.3f}, {:.3f}, {:.3f}, order={})'.format(
            *self.__values__, self.order)

    @staticmethod
    def from_matrix4(matrix4, order=xyz):
        result = Euler(order=order)
        euler_from_matrix4(matrix4, order, result)
        return result

    @staticmethod
    def from_quaternion(quaternion, order=xyz):
        result = Euler(order=order)
        matrix4_from_quaternion(quaternion, matrix4_0)
        euler_from_matrix4(matrix4_0, order, result)
        return result

    def reorder(self, order=xyz):
        result = Euler(order=order)
        quaternion_from_euler(self, self.order, quaternion_0)
        matrix4_from_quaternion(quaternion_0, matrix4_0)
        euler_from_matrix4(matrix4_0, order, result)
        return result


class Vector4(Array):
    __length__ = 4

    def __add__(self, other):
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_add_scalar(self, other, result)
        elif isinstance(other, Vector4):
            vector4_add_vector4(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __radd__(self, other):
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_add_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_sub_scalar(self, other, result)
        elif isinstance(other, Vector4):
            vector4_sub_vector4(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rsub__(self, other):  # 等于加上相反数，再使用加法交换律
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_negate(self, result)
            vector4_add_scalar(result, other, result)
        else:
            raise NotImplementedError

        return result

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_mul_scalar(self, other, result)
        elif isinstance(other, Matrix4):
            vector4_mul_matrix4(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rmul__(self, other):
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_mul_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        result = Vector4()

        if isinstance(other, (float, int)):
            vector4_div_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rtruediv__(self, other):
        raise NotImplementedError

    def __itruediv__(self, other):
        return self.__truediv__(other)

    @staticmethod
    def min(self, other):
        result = Vector4()
        vector4_min_vector4(self, other, result)
        return result

    @staticmethod
    def max(self, other):
        result = Vector4(self)
        vector4_max_vector4(self, other, result)
        return result

    def clamp(self, other_min, other_max):
        result = Vector4()
        if isinstance(other_min, Vector4):  # and other_max
            vector4_clamp_vector4(self, other_min, other_max, result)
        elif isinstance(other_min, (float, int)):  # and other_max
            vector4_clamp_scalar(self, other_min, other_max, result)
        return result

    def clamp_length(self, other_min, other_max):
        result = Vector4()
        vector4_clamp_length(self, other_min, other_max, result)
        return result

    def __floor__(self):
        result = Vector4()
        vector4_floor(self, result)
        return result

    def __ceil__(self):
        result = Vector4()
        vector4_ceil(self, result)
        return result

    def __round__(self):
        result = Vector4()
        vector4_round(self, result)
        return result

    def __trunc__(self):
        result = Vector4()
        vector4_trunc(self, result)
        return result

    def __neg__(self):
        result = Vector4()
        vector4_negate(self, result)
        return result

    def __and__(self, other):  # 用 & 表示点乘 dot
        return vector4_dot_vector4(self, other)

    @property
    def length(self):
        return vector4_length(self)

    @property
    def length_squared(self):
        return vector4_length_squared(self)

    @property
    def length_manhattan(self):
        return vector4_length_manhattan(self)

    def normalize(self):
        result = Vector4()
        vector4_normalize(self, result)
        return result

    @staticmethod
    def from_quaternion(quaternion):
        result = Vector4()
        vector4_from_quaternion(quaternion, result)
        return result

    @staticmethod
    def from_matrix4(matrix4):
        result = Vector4()
        vector4_from_matrix4(matrix4, result)
        return result


class Quaternion(Array):  # 四元数需要保证时常 normalize
    __length__ = 4

    @staticmethod
    def from_euler(euler):
        result = Quaternion()
        quaternion_from_euler(euler, euler.order, result)
        return result

    @staticmethod
    def from_axis_angle(axis_angle):
        result = Quaternion()
        quaternion_from_axis_angle(axis_angle, result)
        return result

    @staticmethod
    def from_matrix4_rotation(matrix4):
        result = Quaternion()
        quaternion_from_matrix4_rotation(matrix4, result)
        return result

    @staticmethod
    def from_unit_vector3(vector3_f, vector3_t):
        result = Quaternion()
        quaternion_from_unit_vector3(vector3_f, vector3_t, result)
        return result

    def angle(self, other):
        return quaternion_angle_to_quaternion(self, other)

    def rotate_towards(self, other, step):
        result = Quaternion()
        quaternion_rotate_towards(self, other, step, result)
        return result

    def conjugate(self):
        result = Quaternion()
        quaternion_conjugate(self, result)
        return result

    def __and__(self, other):
        return quaternion_dot_quaternion(self, other)

    def __mul__(self, other):
        result = Quaternion()

        if isinstance(other, Quaternion):
            quaternion_mul_quaternion(self, other, result)
        else:
            raise NotImplementedError

        return result

    @property
    def length(self):
        return quaternion_length(self)

    @property
    def length_squared(self):
        return quaternion_length_squared(self)

    def normalize(self):
        result = Quaternion()
        quaternion_normalize(self, result)
        return result


class Matrix3(Array):
    __length__ = 9

    def __mul__(self, other):
        result = Matrix3()

        if isinstance(other, (float, int)):
            matrix3_mul_scalar(self, other, result)
        elif isinstance(other, Matrix3):
            matrix3_mul_matrix3(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rmul__(self, other):
        result = Matrix3()

        if isinstance(other, (float, int)):
            matrix3_mul_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __imul__(self, other):
        return self.__mul__(other)

    def scale(self, sx, sy):
        result = Matrix3()
        matrix3_scale(self, sx, sy, result)
        return result

    def rotate(self, theta):
        result = Matrix3()
        matrix3_rotate(self, theta, result)
        return result

    def translate(self, tx, ty):
        result = Matrix3()
        matrix3_translate(self, tx, ty, result)
        return result

    @property
    def determinant(self):
        return matrix3_determinant(self)

    @property
    def inverse(self):
        result = Matrix3()
        matrix3_inverse(self, result)
        return result

    @property
    def transpose(self):
        result = Matrix3()
        matrix3_transpose(self, result)
        return result

    @staticmethod
    def from_identity():
        result = Matrix3()
        matrix3_from_identity(result)
        return result

    @staticmethod
    def from_matrix4(matrix4):
        result = Matrix3()
        matrix3_from_matrix4(matrix4, result)
        return result

    @staticmethod
    def from_matrix4_normal(matrix4):
        result = Matrix3()
        matrix3_from_matrix4(matrix4, result)
        matrix3_inverse(result, result)
        matrix3_transpose(result, result)
        return result

    @staticmethod
    def from_uv_transform(tx, ty, sx, sy, rotation, cx, cy):
        result = Matrix3()
        matrix3_from_uv_transform(tx, ty, sx, sy, rotation, cx, cy, result)
        return result


class Matrix4(Array):
    __length__ = 16

    def __mul__(self, other):
        result = Matrix4()

        if isinstance(other, (float, int)):
            matrix4_mul_scalar(self, other, result)
        elif isinstance(other, Matrix4):
            matrix4_mul_matrix4(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __rmul__(self, other):
        result = Matrix4()

        if isinstance(other, (float, int)):
            matrix4_mul_scalar(self, other, result)
        else:
            raise NotImplementedError

        return result

    def __imul__(self, other):
        return self.__mul__(other)

    @property
    def basis(self):
        return (Vector3(self[0], self[1], self[2]),
                Vector3(self[4], self[5], self[6]),
                Vector3(self[8], self[9], self[10]))

    @basis.setter
    def basis(self, axis):
        axis_a, axis_b, axis_c = axis
        matrix4_from_basis(axis_a, axis_b, axis_c, self)

    @property
    def determinant(self):
        return matrix4_determinant(self)

    @property
    def transpose(self):
        result = Matrix4()
        matrix4_transpose(self, result)
        return result

    @property
    def inverse(self):
        result = Matrix4()
        matrix4_inverse(self, result)
        return result

    def scale_vector3(self, vector3):
        result = Matrix4()
        matrix4_scale_vector3(self, vector3, result)
        return result

    @property
    def max_scale(self):
        return matrix4_max_scale(self)

    @staticmethod
    def from_identity():
        result = Matrix4()
        matrix4_from_identity(result)
        return result

    @staticmethod
    def from_euler(euler):
        result = Matrix4()
        matrix4_from_euler(euler, euler.order, result)
        return result

    @staticmethod
    def from_quaternion(quaternion):
        result = Matrix4()
        matrix4_from_quaternion(quaternion, result)
        return result

    @staticmethod
    def from_look_at(eye, target, up):
        result = Matrix4()

        if isinstance(eye, tuple):
            matrix4_from_look_at(Vector3(*eye), Vector3(*target),
                                 Vector3(*up), result)
        elif isinstance(eye, Vector3):
            matrix4_from_look_at(eye, target, up, result)
        else:
            raise NotImplementedError

        return result

    @staticmethod
    def from_translation(x, y, z):
        result = Matrix4()
        matrix4_from_translation(x, y, z, result)
        return result

    @staticmethod
    def from_rotation_x(theta):
        result = Matrix4()
        matrix4_from_rotation_x(theta, result)
        return result

    @staticmethod
    def from_rotation_y(theta):
        result = Matrix4()
        matrix4_from_rotation_y(theta, result)
        return result

    @staticmethod
    def from_rotation_z(theta):
        result = Matrix4()
        matrix4_from_rotation_z(theta, result)
        return result

    @staticmethod
    def from_rotation(other):
        result = Matrix4()

        if isinstance(other, Matrix3):
            matrix4_from_matrix3_as_rotation(other, result)
        elif isinstance(other, Vector4):
            matrix4_from_rotation(other, other[3], result)
        else:
            raise NotImplementedError

        return result

    @staticmethod
    def from_scale(x, y, z):
        result = Matrix4()
        matrix4_from_scale(x, y, z, result)
        return result

    @staticmethod
    def from_shear(x, y, z):
        result = Matrix4()
        matrix4_from_shear(x, y, z, result)
        return result

    @staticmethod
    def from_compose(position, rotation, scale):
        result = Matrix4()
        matrix4_from_compose(position, rotation, scale, result)
        return result

    def to_compose(self):
        position, rotation, scale = Vector3(), Quaternion(), Vector3()
        matrix4_to_decompose(self, position, rotation, scale)
        return position, rotation, scale

    @staticmethod
    def from_perspective_bounds(left, right, bottom, top, near, far):
        result = Matrix4()
        matrix4_from_perspective_bounds(
            left, right, bottom, top, near, far, result)
        return result

    @staticmethod
    def from_perspective(fov, aspect, near, far):
        result = Matrix4()
        _semi_y = near * math.tan(math.radians(fov / 2))
        _semi_x = _semi_y * aspect
        matrix4_from_perspective_bounds(-_semi_x, _semi_x, -_semi_y,
                                        _semi_y, near, far, result)
        return result

    @staticmethod
    def from_orthogonal(left, right, bottom, top, near, far):
        result = Matrix4()
        matrix4_from_orthogonal(left, right, bottom, top, near, far, result)
        return result


__all__ = [
    'Array', 'non_zero', 'clamp', 'xyz', 'yxz', 'zxy', 'zyx', 'yzx', 'xzy',
    'distance', 'distance_squared', 'distance_manhattan', 'interpolation',
    'float_nan', 'float_inf', 'float_max', 'float_min', 'Matrix3', 'Matrix4',
    'Vector2', 'Vector3', 'Vector4', 'Euler', 'Quaternion'
]

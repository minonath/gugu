import math
from .multi_dimensional_array import *
from .multi_dimensional_array.makefile import *

cache_vector2_0 = Vector2()
cache_vector2_1 = Vector2()
cache_vector2_2 = Vector2()
cache_vector3_0 = Vector3()
cache_vector3_1 = Vector3()
cache_vector3_2 = Vector3()


class Point(Vector3):
    pass


class Line(object):
    def __init__(self, start, end):
        self.line_start = Vector3(*start)
        self.line_end = Vector3(*end)

    def __repr__(self):
        return 'Line(start={} end={})'.format(self.line_start, self.line_end)


class Ray(object):  # Ray 可以看作是个长度为 1 的线段
    def __init__(self, origin, direction):  # direction 需要为 normalize
        self.ray_origin = Vector3(*origin)
        self.ray_direction = Vector3(*direction)

    def __repr__(self):
        return 'Ray(origin={} direction={})'.format(
            self.ray_origin, self.ray_direction)


class Triangle(object):
    def __init__(self, point_a, point_b, point_c):
        self.triangle_a = Vector3(*point_a)
        self.triangle_b = Vector3(*point_b)
        self.triangle_c = Vector3(*point_c)

    def __repr__(self):
        return 'Triangle(a={} b={} c={})'.format(
            self.triangle_a, self.triangle_b, self.triangle_c)


class Plane(object):
    def __init__(self, normal, constant):
        self.plane_normal = Vector3(*normal)
        self.plane_constant = constant

    def __repr__(self):
        return 'Plane(normal={} constant={})'.format(
            self.plane_normal, self.plane_constant)


class Box(object):
    def __init__(self, point_min, point_max):
        self.box_min = Vector3(*point_min)
        self.box_max = Vector3(*point_max)

    def __repr__(self):
        return 'Box(min={} max={})'.format(
            self.box_min, self.box_max)


class Sphere(object):
    def __init__(self, center, radius):
        self.sphere_center = Vector3(*center)
        self.sphere_radius = radius

    def __repr__(self):
        return 'Sphere(center={} radius={})'.format(
            self.sphere_center, self.sphere_radius)


def point_cylindrical_from_cartesian(point: Point):
    """
    将 Point 从笛卡尔坐标转换为圆柱体坐标
    右手坐标为顺时针，左手坐标为逆时针 y 轴向上
    (x, y, z) => (radius, polar-angle, y-coordinate)
    """
    x, y, z = point
    return Vector3((x * x + z * z) ** 0.5, math.atan2(x, z), y)


def point_spherical_from_cartesian(point: Vector3):
    """
    将 Point 从笛卡尔坐标转换为球面坐标
    右手坐标为顺时针，左手坐标为逆时针 y 轴向上
    (x, y, z) => (radius, polar-angle, azimuthal-angle)
    """
    x, y, z = point
    radius = (x * x + y * y + z * z) ** 0.5
    if radius:
        return Vector3(
            radius, math.atan2(x, z), math.acos(clamp(y / radius, - 1, 1))
        )
    else:
        return Vector3()  # 原点

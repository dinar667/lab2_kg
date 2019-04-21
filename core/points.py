# coding: utf-8

import numpy as np
from math import sqrt

from core.matrix import Matrix


class Point2D(object):
    def __init__(self, x: float = 0, y: float = 0):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value) -> None:
        self._y = value

    def __str__(self) -> str:
        return f"Point2D ({self._x}, {self._y})"

    def __add__(self, point) -> "Point2D":
        return Point2D(self._x + point.x, self._y + point.y)

    def __sub__(self, point) -> "Point2D":
        return Point2D(self._x - point.x, self._y - point.y)


class Point3D(Point2D):
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        super().__init__(x, y)

        self._z: float = z

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value) -> None:
        self._z = value

    def __str__(self) -> str:
        return f"Point3D ({self._x}; {self._y}; {self._z})"

    def to_2d_xy(self) -> Point2D:
        return Point2D(self._x, self._y)

    def get_prod(self, point) -> float:
        """ Скалярное произведение точек """
        return self._x * point.x + self._y * point.y + self._z * point.z

    def __mul__(self, matrix: Matrix) -> "Point3D":
        v = np.array([self.x, self.y, self.z, 1])
        result_matrix = np.dot(v, matrix.values)

        x, y, z, w = result_matrix
        return Point3D(x, y, z).normalized(w)

    def __bool__(self) -> bool:
        return any((self.x, self.y, self.z))

    def __eq__(self, point: "Point3D"):
        return self.x == point.x and self.y == point.y and self.z == point.z

    def normalized(self, w: float) -> "Point3D":
        if w == 0:
            w = 1
        return Point3D(self.x / w, self.y / w, 1)

    def in_origin(self) -> bool:
        """ Точка в начале координат"""
        return self.x == 0 and self.y == 0 and self.z == 0

    def inside(self, point: "Point3D") -> bool:
        """
        Текущая точка находится за другой точкой (внутри параллелепипеда)
        """
        return self.x <= point.x and self.y <= point.y and self.z <= point.z

    def module(self) -> float:
        """ Модуль вектора """
        return sqrt(self._x * self._x + self._y * self._y + self._z * self._z)

    def cos_between(self, point: "Point3D") -> float:
        """
        Находит косинус между текущим вектором и вектором до точки point
        """
        mul_modules = self.module() * point.module()
        if mul_modules == 0:
            return 0
        prod = (point.x - self.x) * (-self.x) + (point.y - self.y) * (-self.y) + (point.z - self.z) * (-self.z)
        return prod / mul_modules

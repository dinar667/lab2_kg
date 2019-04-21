# coding: utf-8

import numpy as np

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

    # Скалярное произведение точек
    def get_prod(self, point) -> float:
        return self._x * point.x + self._y * point.y + self._z * point.z

    def __mul__(self, matrix: Matrix) -> "Point3D":
        v = np.array([self.x, self.y, self.z, 1])
        result_matrix = np.dot(v, matrix.values)

        x, y, z, w = result_matrix
        return Point3D(x, y, z).normalized(w)

    def __bool__(self) -> bool:
        return any((self.x, self.y, self.z))

    def normalized(self, w: float) -> "Point3D":
        if w == 0:
            w = 1
        return Point3D(self.x / w, self.y / w, 1)

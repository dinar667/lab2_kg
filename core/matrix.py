# coding: utf-8

import numpy as np


class Matrix(object):
    """ Работа с матрицей """

    def __init__(self, width: int = 4, height: int = 4, input_values=None):

        # Столбцов в матрице
        self._width: int = width

        # Строк в матрице
        self._height: int = height

        self._values: np.ndarray = np.zeros((width, height), dtype=np.float64)

        if input_values is not None:
            self._values = np.array(input_values)
            self._width, self._height = self._values.shape

    def __str__(self):
        return f"{self._values}"

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def values(self):
        return self._values

    def get_value(self, x: int, y: int):
        return self._values[x, y]

    # ---
    # Работа с массивом данных

    @values.setter
    def values(self, values):
        self._values = np.array(values)
        self._width, self._height = self._values.shape

    def set_value(self, x: int, y: int, value):
        self._values[x, y] = value

    # ---
    # Операторы

    # Сложение
    def __add__(self, other: "Matrix"):
        matrix = Matrix()
        matrix.values = np.add(self.values, other.values)
        return matrix

    # Вычитание
    def __sub__(self, other: "Matrix"):
        matrix = Matrix()
        matrix.values = np.subtract(self.values, other.values)
        return matrix

    # Умножение
    def __mul__(self, other: "Matrix"):
        matrix = Matrix()
        matrix.values = np.dot(self.values, other.values)
        return matrix

    # Транспонирование
    def transposed(self):
        matrix = Matrix()
        matrix.values = np.transpose(self.values)
        return matrix

    # Обратная матрица
    def inverted(self):
        matrix = Matrix()
        matrix.values = np.linalg.inv(self.values)
        return matrix

    # ---


if __name__ == "__main__":
    m1 = Matrix()
    m1.values = [[1, 2], [3, 4]]
    print(m1)

    m2 = Matrix()
    m2.values = [[2, 0], [3, 4]]
    print(m2)

    print(m1 + m2)
    print(m1 - m2)
    print(m1 * m2)

    print(m1.transposed())
    print(m1.inverted())

    m3 = Matrix(2, 2, [[1, 2], [3, 4]])
    print(m3)

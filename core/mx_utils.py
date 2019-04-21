# coding: utf-8

from core.matrix import Matrix


def get_eye() -> Matrix:
    """
    Возвращает единичную матрицу
    :return:
    """
    return Matrix(input_values=[
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def get_matrix_rx(c: float, s: float) -> Matrix:
    """ Поворот вокруг оси X """

    rx_values = [
        [1, 0, 0, 0],
        [0, c, s, 0],
        [0, -s, c, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=rx_values)


def get_matrix_ry(c: float, s: float) -> Matrix:
    """ Поворот вокруг оси Y """

    ry_values = [
        [c, 0, -s, 0],
        [0, 1, 0, 0],
        [s, 0, c, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=ry_values)


def get_matrix_rz(c: float, s: float) -> Matrix:
    """ Поворот вокруг Z """

    rz_values = [
        [c, s, 0, 0],
        [-s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=rz_values)


def get_matrix_d(alpha: float, beta: float, gamma: float) -> Matrix:
    """ Матрица растяжения (сжатия) """

    d_values = [
        [alpha, 0, 0, 0],
        [0, beta, 0, 0],
        [0, 0, gamma, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=d_values)


def get_matrix_mx() -> Matrix:
    """ Отражение относительно оси yOz """

    values = [
        [-1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=values)


def get_matrix_my() -> Matrix:
    """ Отражение относительно оси zOx """

    values = [
        [1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=values)


def get_matrix_mz() -> Matrix:
    """ Отражение относительно оси xOy """

    values = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=values)


def get_matrix_t(lam, mu, nu) -> Matrix:
    """ Перенос (сдвиг, смещение) на вектор (lam, mu, nu) """

    values = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [lam, mu, nu, 1]
    ]
    return Matrix(input_values=values)


def get_matrix_pz() -> Matrix:
    values = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=values)


def get_matrix_p(c: float) -> Matrix:
    values = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, -1/c],
        [0, 0, 0, 1]
    ]
    return Matrix(input_values=values)

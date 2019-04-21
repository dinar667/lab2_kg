# coding: utf-8

import enum
from functools import reduce
from operator import mul
from typing import Dict, List

from PyQt5 import QtCore, QtGui, QtWidgets
from math import sqrt

from core.mx_utils import *
from core.points import Point3D
from gui.plane_systems.ax_plane_system import AxonometricPlaneSystem
from gui.plane_systems.cx_plane_system import ComplexPlaneSystem
from gui.settings import *
from gui.ui_main_window import Ui_MainWindow


class SelectPoint(enum.Enum):
    """
    Выбираемые точки:

    - `T` - точка T
    - `C` - точка C (камера)
    """

    C = enum.auto()
    T = enum.auto()


class SelectProjection(enum.Enum):
    """
    Выбираемое проецирование:

    - `CEN` - центральное
    - `ORT` - ортогональное
    """

    CEN = enum.auto()
    ORT = enum.auto()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.setupUi(self)

        self.axis_length: int = 100

        # Координаты точки T
        self.xT: int = POINT_XT
        self.yT: int = POINT_YT
        self.zT: int = POINT_ZT

        # Координаты точки C (Камеры)
        self.xC: int = POINT_XC
        self.yC: int = POINT_YC
        self.zC: int = POINT_ZC

        self.selected_projection: SelectProjection = SelectProjection.ORT
        self.selected_point: SelectPoint = SelectPoint.T

        # Точки 3D
        self.points_3d: Dict[str, Point3D] = {}

        # Точки аксонометрического чертежа
        self.points_2d_ax: Dict[str, QtCore.QPointF] = {}

        # Точки комплексного чертежа
        self.points_2d_cx: Dict[str, QtCore.QPointF] = {}

        # Координатные системы
        self.aps = AxonometricPlaneSystem(self.awidget)
        self.cps = ComplexPlaneSystem(self.cwidget)

        # Задаем значения по умолчанию
        self.setup_fields()

    def setup_fields(self) -> None:
        self.change_slider_values(POINT_XT, POINT_YT, POINT_ZT)

        self.xTField.setText(f"{POINT_XT}")
        self.yTField.setText(f"{POINT_YT}")
        self.zTField.setText(f"{POINT_ZT}")

        self.xCField.setText(f"{POINT_XC}")
        self.yCField.setText(f"{POINT_YC}")
        self.zCField.setText(f"{POINT_ZC}")

        self.radioT.setChecked(True)
        self.radioOrhogonal.setChecked(True)

    @QtCore.pyqtSlot(int, name="on_x_changed")
    def on_x_changed(self, value):
        if self.selected_point == SelectPoint.T:
            self.xT = value
            self.xTField.setText(f"{value}")
        elif self.selected_point == SelectPoint.C:
            self.xC = value
            self.xCField.setText(f"{value}")
        self.on_coordinate_changed()

    @QtCore.pyqtSlot(int, name="on_y_changed")
    def on_y_changed(self, value):
        if self.selected_point == SelectPoint.T:
            self.yT = value
            self.yTField.setText(f"{value}")
        elif self.selected_point == SelectPoint.C:
            self.yC = value
            self.yCField.setText(f"{value}")
        self.on_coordinate_changed()

    @QtCore.pyqtSlot(int, name="on_z_changed")
    def on_z_changed(self, value):
        if self.selected_point == SelectPoint.T:
            self.zT = value
            self.zTField.setText(f"{value}")
        elif self.selected_point == SelectPoint.C:
            self.zC = value
            self.zCField.setText(f"{value}")
        self.on_coordinate_changed()

    @QtCore.pyqtSlot(name="on_radio_t_clicked")
    def on_radio_t_clicked(self):
        if self.selected_point == SelectPoint.C:
            self.selected_point = SelectPoint.T
            self.change_slider_values(self.xT, self.yT, self.zT)
            self.on_selected_point_changed()

    @QtCore.pyqtSlot(name="on_radio_c_clicked")
    def on_radio_c_clicked(self):
        if self.selected_point == SelectPoint.T:
            self.selected_point = SelectPoint.C
            self.change_slider_values(self.xC, self.yC, self.zC)
            self.on_selected_point_changed()

    def change_slider_values(self, x, y, z):
        self.xSlider.setValue(x)
        self.ySlider.setValue(y)
        self.zSlider.setValue(z)

    @QtCore.pyqtSlot(name="on_selected_projection_radio_clicked")
    def on_radio_central_clicked(self):
        if self.selected_projection == SelectProjection.ORT:
            self.selected_projection = SelectProjection.CEN
            self.on_projection_changed()

    def on_radio_orthogonal_clicked(self):
        if self.selected_projection == SelectProjection.CEN:
            self.selected_projection = SelectProjection.ORT
            self.on_projection_changed()

    # ----
    # Далее функции для работы с чертежами
    # ----

    def on_coordinate_changed(self):

        # Заполняем массив координат
        self.fill_3d_coordinates()

        # Пересчитываем все точки
        self.recalculate_all()

        # Отрисовываем результат
        self.draw_result()

    def on_selected_point_changed(self):
        self.recalculate_ax_coordinates()
        self.draw_ax_plane()

    def on_projection_changed(self):
        self.fill_3d_coordinates()
        self.recalculate_ax_coordinates()
        self.draw_ax_plane()

    def fill_3d_coordinates(self):
        x, y, z = self.xT, self.yT, self.zT

        self.points_3d["T"] = Point3D(x, y, z)
        self.points_3d["0"] = Point3D(0, 0, 0)

        self.points_3d["TX"] = Point3D(x, 0, 0)
        self.points_3d["TY"] = Point3D(0, y, 0)
        self.points_3d["TZ"] = Point3D(0, 0, z)

        self.points_3d["T1"] = Point3D(x, y, 0)
        self.points_3d["T2"] = Point3D(0, y, z)
        self.points_3d["T3"] = Point3D(x, 0, z)

        self.points_3d["TX"] = Point3D(x, 0, 0)
        self.points_3d["TY"] = Point3D(0, y, 0)
        self.points_3d["TZ"] = Point3D(0, 0, z)

        self.points_3d["+X"] = Point3D(self.axis_length, 0, 0)
        self.points_3d["+Y"] = Point3D(0, self.axis_length, 0)
        self.points_3d["+Z"] = Point3D(0, 0, self.axis_length)

    def recalculate_all(self):
        self.recalculate_ax_coordinates()
        self.recalculate_ep_coordinates()

    def recalculate_ax_coordinates(self):
        """
        Пересчитываем из 3D в координаты экрана
        (для аксонометрического чертежа)
        """

        if self.is_central_projection():
            can_be_drawn = self.cx_can_be_drawn()
        else:
            can_be_drawn = self.ax_can_be_drawn()

        if not can_be_drawn:
            return

        self.aps.error = False

        # координаты камеры
        x, y, z = self.xC, self.yC, self.zC

        sqrt_xy: float = sqrt(x * x + y * y)
        sqrt_xyz: float = sqrt(x * x + y * y + z * z)

        if sqrt_xyz == 0:
            return

        if sqrt_xy == 0:
            sin_phi = 0
            cos_phi = 1
        else:
            cos_phi = y / sqrt_xy
            sin_phi = x / sqrt_xy

        cos_psi: float = z / sqrt_xyz
        sin_psi: float = sqrt_xy / sqrt_xyz

        # Массив матриц преобразований
        ops: List[Matrix] = []

        # Матрица поворота системы координат на угол phi вокруг оси Z
        rz_matrix: Matrix = get_matrix_rz(cos_phi, sin_phi)
        ops.append(rz_matrix)

        # Матрица поворота системы координат на угол psi вокруг оси X
        rx_matrix: Matrix = get_matrix_rx(cos_psi, sin_psi)
        ops.append(rx_matrix)

        # Матрица зеркального отображения относительно yOZ
        mx_matrix: Matrix = get_matrix_mx()
        ops.append(mx_matrix)

        # Если выбрано центральное проецирование
        if self.is_central_projection():
            pr_matrix: Matrix = get_matrix_p(sqrt_xyz)
            ops.append(pr_matrix)

        # Матрица проецирования на плоскость xOy
        p_matrix: Matrix = get_matrix_pz()
        ops.append(p_matrix)

        # Матрица переноса в начало координат
        t_matrix: Matrix = get_matrix_t(
            self.awidget.width() // 2, self.awidget.height() // 2, 0
        )
        ops.append(t_matrix)

        product: Matrix = self.calculate_transform(ops)
        self.apply_matrix(product)

    @staticmethod
    def calculate_transform(ops: List[Matrix]) -> Matrix:
        return reduce(mul, ops)

    def apply_matrix(self, matrix: Matrix) -> None:
        for pname, point in self.points_3d.items():
            self.points_2d_ax[pname] = self.from_3d_to_ax_scene(point, matrix)

    def recalculate_ep_coordinates(self):
        """ Пересчитываем из 3D в координаты чертежа """

        # "служебные"
        self.points_2d_cx["0"] = QtCore.QPointF(0, 0)
        self.points_2d_cx["+X -Y"] = QtCore.QPointF(-self.axis_length, 0)
        self.points_2d_cx["-X +Y"] = QtCore.QPointF(self.axis_length, 0)
        self.points_2d_cx["+Z -Y"] = QtCore.QPointF(0, -self.axis_length)
        self.points_2d_cx["-Z +Y"] = QtCore.QPointF(0, self.axis_length)

        # для точки T
        x_t, y_t, z_t = self.xT, self.yT, self.zT
        self.points_2d_cx["T1"] = QtCore.QPointF(-x_t, y_t)
        self.points_2d_cx["T2"] = QtCore.QPointF(-x_t, -z_t)
        self.points_2d_cx["T3"] = QtCore.QPointF(y_t, -z_t)

        self.points_2d_cx["TX"] = QtCore.QPointF(-x_t, 0)
        self.points_2d_cx["TY1"] = QtCore.QPointF(0, y_t)
        self.points_2d_cx["TY3"] = QtCore.QPointF(y_t, 0)
        self.points_2d_cx["TZ"] = QtCore.QPointF(0, -z_t)

        # для точки C
        x_c, y_c, z_c = self.xC, self.yC, self.zC
        self.points_2d_cx["C1"] = QtCore.QPointF(-x_c, y_c)
        self.points_2d_cx["C2"] = QtCore.QPointF(-x_c, -z_c)
        self.points_2d_cx["C3"] = QtCore.QPointF(y_c, -z_c)

        self.points_2d_cx["CX"] = QtCore.QPointF(-x_c, 0)
        self.points_2d_cx["CY1"] = QtCore.QPointF(0, y_c)
        self.points_2d_cx["CY3"] = QtCore.QPointF(y_c, 0)
        self.points_2d_cx["CZ"] = QtCore.QPointF(0, -z_c)

    def draw_result(self):
        self.draw_ax_plane()
        self.draw_cx_plane()

    def draw_ax_plane(self):
        self.aps.update_plane(self.points_2d_ax)

    def draw_cx_plane(self):
        self.cps.update_plane(self.points_2d_cx)

    # ----
    @staticmethod
    def from_3d_to_ax_scene(point: Point3D, product: Matrix) -> QtCore.QPointF:
        p = point * product
        return QtCore.QPointF(p.x, p.y)

    def showEvent(self, e: QtGui.QShowEvent) -> None:
        super().showEvent(e)
        # Вызываем первую отрисовку
        self.on_coordinate_changed()
        self.on_projection_changed()

    # ПРОВЕРКИ

    def is_central_projection(self) -> bool:
        """ Текущая проекция - центральная """
        return self.selected_projection == SelectProjection.CEN

    def ax_can_be_drawn(self) -> bool:
        """
        Проверка на возможность отрисовки точки при ортогональном проецировании
        """
        camera: Point3D = Point3D(self.xC, self.yC, self.zC)

        if camera.in_origin():
            self.draw_ax_error(
                "Проекции не существует: камера в начале координат"
            )
            return False

        return True

    def cx_can_be_drawn(self) -> bool:
        """
        Проверка на возможность отрисовки точки при центральном проецировании
        """

        camera: Point3D = Point3D(self.xC, self.yC, self.zC)

        # Если камера в начале координат
        if camera.in_origin():
            self.draw_ax_error(
                "Проекции не существует: камера в начале координат"
            )
            return False

        tpoint: Point3D = Point3D(self.xT, self.yT, self.zT)
        # Координаты камеры равны точке T
        if camera.equals(tpoint):
            self.draw_ax_error(
                "Проекции не существует: "
                "координаты точки и камеры совпадают."
            )
            return False

        # Если камера внутри прямоугольника
        if camera.inside(tpoint):
            self.draw_ax_error("Камера внутри")
            return False

        # Проекции между камерой и плоскостю не существует
        if camera.cos_between(tpoint) <= 0:
            self.draw_ax_error("Проекция точки не лежит в плоскости экрана")
            return False

        return True

    def draw_ax_error(self, text: str) -> None:
        """ Показывает ошибку на аксонометрическом чертеже """
        self.aps.show_error(text)

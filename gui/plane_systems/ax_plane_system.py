# coding: utf-8

from PyQt5 import QtCore, QtGui, QtWidgets

from gui.base.base_plane_system import BasePlaneSystem


class AxonometricPlaneSystem(BasePlaneSystem):
    def __init__(self, widget: QtWidgets.QWidget) -> None:
        super().__init__(widget)

        # Цвета осей координат
        self.x_line_color = QtGui.QColor("blue")
        self.y_line_color = QtGui.QColor("green")
        self.z_line_color = QtGui.QColor("red")

        # Кисти для осей координат
        self.x_line_pen = QtGui.QPen(self.x_line_color, self.line_width)
        self.dashed_x_line_pen = QtGui.QPen(
            self.x_line_color, self.line_width, QtCore.Qt.DashLine
        )

        self.y_line_pen = QtGui.QPen(self.y_line_color, self.line_width)
        self.dashed_y_line_pen = QtGui.QPen(
            self.y_line_color, self.line_width, QtCore.Qt.DashLine
        )

        self.z_line_pen = QtGui.QPen(self.z_line_color, self.line_width)
        self.dashed_z_line_pen = QtGui.QPen(
            self.z_line_color, self.line_width, QtCore.Qt.DashLine
        )

    def update_pixmap(self) -> None:
        painter: QtGui.QPainter = QtGui.QPainter(self.pixmap)
        painter.begin(self.pixmap)

        # Включаем склаживание
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setBrush(self.point_brush)
        painter.drawRect(0, 0, self.widget.width(), self.widget.height())

        painter.setBackground(self.point_brush)

        if not self.points:
            return

        # Рисуем все оси
        self.draw_all_axis(painter)

        # Рисуем линии параллелепипеда
        self.draw_lines(painter)

        # Рисуем точки
        self.draw_points(painter)

        # painter.end()     # вызывается автоматически

    def draw_all_axis(self, painter: QtGui.QPainter) -> None:
        """ Рисует оси координат """

        self.draw_x_axis(painter)
        self.draw_y_axis(painter)
        self.draw_z_axis(painter)

    def draw_x_axis(self, painter: QtGui.QPainter) -> None:
        axis: QtCore.QLineF = self.get_line(
            self.points["+X"], self.points["0"]
        )
        self.draw_axis(painter, axis, self.x_line_pen, self.dashed_x_line_pen)

    def draw_y_axis(self, painter: QtGui.QPainter) -> None:
        axis: QtCore.QLineF = self.get_line(
            self.points["+Y"], self.points["0"]
        )
        self.draw_axis(painter, axis, self.y_line_pen, self.dashed_y_line_pen)

    def draw_z_axis(self, painter: QtGui.QPainter) -> None:
        axis: QtCore.QLineF = self.get_line(
            self.points["+Z"], self.points["0"]
        )
        self.draw_axis(painter, axis, self.z_line_pen, self.dashed_z_line_pen)

    def draw_lines(self, painter: QtGui.QPainter) -> None:
        """ Рисует линии параллелепипеда """

        # переключаем кисть
        painter.setPen(self.label_pen)
        painter.setBackground(QtCore.Qt.white)

        painter.drawLine(self.points["T"], self.points["T1"])
        painter.drawLine(self.points["T"], self.points["T2"])
        painter.drawLine(self.points["T"], self.points["T3"])

        painter.drawLine(self.points["T1"], self.points["TX"])
        painter.drawLine(self.points["T1"], self.points["TY"])

        painter.drawLine(self.points["T2"], self.points["TY"])
        painter.drawLine(self.points["T2"], self.points["TZ"])

        painter.drawLine(self.points["T3"], self.points["TX"])
        painter.drawLine(self.points["T3"], self.points["TZ"])

        painter.drawLine(self.points["TX"], self.points["0"])
        painter.drawLine(self.points["TY"], self.points["0"])
        painter.drawLine(self.points["TZ"], self.points["0"])

    def show_error(self, text: str) -> None:
        self.error = True
        painter: QtGui.QPainter = QtGui.QPainter(self.pixmap)
        painter.begin(self.pixmap)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(self.point_brush)
        painter.drawRect(0, 0, self.widget.width(), self.widget.height())

        painter.setBackground(self.point_brush)

        painter.drawText(
            QtCore.QRect(0, 0, self.widget.width(), self.widget.height()),
            QtCore.Qt.AlignCenter,
            text
        )

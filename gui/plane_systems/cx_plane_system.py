# coding: utf-8

from PyQt5 import QtCore, QtGui, QtWidgets

from gui.base.base_plane_system import BasePlaneSystem


class ComplexPlaneSystem(BasePlaneSystem):
    def __init__(self, widget: QtWidgets.QWidget) -> None:
        super().__init__(widget)

        # Цвета оси координат XY
        self.xy_x_line_color = QtGui.QColor("blue")
        self.xy_y_line_color = QtGui.QColor("green")

        # Цвета оси координат YZ
        self.zy_y_line_color = QtGui.QColor("green")
        self.zy_z_line_color = QtGui.QColor("red")

        # Кисти для рисования осей координат
        self.xy_x_line_pen = QtGui.QPen(self.xy_x_line_color, self.line_width)
        self.xy_y_line_pen = QtGui.QPen(self.xy_y_line_color, self.line_width)
        self.zy_y_line_pen = QtGui.QPen(self.zy_y_line_color, self.line_width)
        self.zy_z_line_pen = QtGui.QPen(self.zy_z_line_color, self.line_width)

        # Цвет линий соединения камеры
        self.c_line_color: QtGui.QColor = QtGui.QColor("blue")
        self.c_label_pen: QtGui.QPen = QtGui.QPen(
            self.c_line_color, self.line_width
        )

    def update_pixmap(self) -> None:
        painter: QtGui.QPainter = QtGui.QPainter(self.pixmap)
        painter.begin(self.pixmap)

        # Включаем сглаживание
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setBrush(self.point_brush)
        painter.drawRect(0, 0, self.widget.width(), self.widget.height())
        painter.setBackground(QtGui.QColor("white"))

        if not self.points:
            painter.end()
            return

        # Переходим в центр координат
        painter.translate(self.xhalf, self.yhalf)

        # рисуем оси
        self.draw_all_axis(painter)

        # рисуем линии
        self.draw_lines(painter)

        # рисуем точки
        self.draw_points(painter)

        painter.end()

    def draw_all_axis(self, painter: QtGui.QPainter) -> None:
        self.draw_xy_axis(painter)
        self.draw_zy_axis(painter)

    def draw_xy_axis(self, painter: QtGui.QPainter) -> None:
        axis = self.get_line(self.points["+X -Y"], self.points["-X +Y"])
        self.draw_axis(painter, axis, self.xy_x_line_pen, self.xy_y_line_pen)

    def draw_zy_axis(self, painter: QtGui.QPainter) -> None:
        axis = self.get_line(self.points["+Z -Y"], self.points["-Z +Y"])
        self.draw_axis(painter, axis, self.zy_z_line_pen, self.zy_y_line_pen)

    def draw_lines(self, painter: QtGui.QPainter) -> None:

        self.draw_c_lines(painter)
        self.draw_t_lines(painter)

    def draw_t_lines(self, painter):
        # переключаем кисть
        painter.setPen(self.label_pen)
        painter.setBackground(QtCore.Qt.white)

        # из TY1 в T1
        painter.drawLine(self.points["TY1"], self.points["T1"])

        # из T1 в TX
        painter.drawLine(self.points["T1"], self.points["TX"])

        # из TX в T2
        painter.drawLine(self.points["TX"], self.points["T2"])

        # из T2 в TZ
        painter.drawLine(self.points["T2"], self.points["TZ"])

        # из TZ в T3
        painter.drawLine(self.points["TZ"], self.points["T3"])

        # Из T3 в TY3
        painter.drawLine(self.points["T3"], self.points["TY3"])

        # рисуем сектор
        self.draw_arc(painter, self.points["TY3"].x(), self.points["TY1"].y())

    def draw_c_lines(self, painter):
        painter.setPen(self.c_label_pen)
        painter.setBackground(QtCore.Qt.white)

        # из TY1 в C1
        painter.drawLine(self.points["CY1"], self.points["C1"])

        # из C1 в CX
        painter.drawLine(self.points["C1"], self.points["CX"])

        # из CX в C2
        painter.drawLine(self.points["CX"], self.points["C2"])

        # из C2 в CZ
        painter.drawLine(self.points["C2"], self.points["CZ"])

        # из CZ в C3
        painter.drawLine(self.points["CZ"], self.points["C3"])

        # Из C3 в CY3
        painter.drawLine(self.points["C3"], self.points["CY3"])

        # рисуем сектор
        self.draw_arc(painter, self.points["CY3"].x(), self.points["CY1"].y())

    @staticmethod
    def draw_arc(painter: QtGui.QPainter, x: int, y: int) -> None:
        angle: int = 90 * 16
        if y > 0:
            angle = 270 * 16

        width: float = -2 * x
        height: float = -2 * y

        span_angle: int = 90 * 16
        painter.drawArc(x, y, width, height, angle, span_angle)

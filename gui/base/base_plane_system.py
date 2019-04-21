# coding: utf-8

from typing import Dict, Callable

from PyQt5 import QtCore, QtGui, QtWidgets


class BasePlaneSystem:
    """
    Базовый класс для систем координат

    Необходимо переопределить следующие методы:

    - `update_pixmap()`

    """

    def __init__(self, widget: QtWidgets.QWidget) -> None:
        self.widget: QtWidgets.QWidget = widget
        self.widget.paintEvent: Callable = self.paint_event
        self.widget.resizeEvent: Callable = self.resize_event

        # Радиус точки (in px)
        self.point_radius: int = 3

        # Кисть для отрисовки точки
        self.point_brush: QtGui.QBrush = QtGui.QBrush(QtCore.Qt.white)

        # Ширина линии
        self.line_width: int = 2

        # Цвет линии
        self.label_color: QtGui.QColor = QtGui.QColor("#000")

        # Кисть для рисования линии
        self.label_pen: QtGui.QPen = QtGui.QPen(
            self.label_color, self.line_width
        )

        # Коорлинаты центра виджета
        self.xhalf: int = 0
        self.yhalf: int = 0

        # Отступ надписи от линии (in px)
        self.label_offset_x: int = 10
        self.label_offset_y: int = 15

        # Массив точек
        self.points: Dict[str, QtCore.QPointF] = {}

        # Т.н. "полотно", на котом рисуется выходное изображение
        self.pixmap: QtGui.QPixmap = QtGui.QPixmap(self.widget.size())

    @staticmethod
    def get_line(
            start: QtCore.QPointF, end: QtCore.QPointF
    ) -> QtCore.QLineF:
        """ Возвращает QLineF по двум точкам """
        return QtCore.QLineF(start.x(), start.y(), end.x(), end.y())

    @staticmethod
    def draw_axis(
            painter: QtGui.QPainter,
            axis: QtCore.QLineF,
            pen: QtGui.QPen,
            dash_pen: QtGui.QPen
    ) -> None:
        """ Рисует координатную ось """
        painter.setPen(pen)
        painter.drawLine(
            int(axis.x1()),
            int(axis.y1()),
            int(axis.x2()),
            int(axis.y2())
        )
        # print(axis.x1(), axis.y1(), axis.x2() // 2, axis.y2() // 2)

        # painter.setPen(pen)
        # painter.drawLine(0, 0, int(axis.x1()), int(axis.y1()))
        # painter.setPen(dash_pen)
        # painter.drawLine(0, 0, int(axis.x2()), int(axis.y2()))

    def update_plane(self, points: Dict[str, QtCore.QPointF]) -> None:
        self.points = points
        self.widget.repaint()

    def paint_event(self, event: QtGui.QPaintEvent) -> None:
        self.update_pixmap()

        painter = QtGui.QPainter(self.widget)
        painter.begin(self.widget)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()

        event.accept()

    def resize_event(self, event: QtGui.QResizeEvent) -> None:
        self.xhalf = self.widget.width() // 2
        self.yhalf = self.widget.height() // 2

        self.pixmap = QtGui.QPixmap(self.widget.size())

        event.accept()

    def draw_points(self, painter: QtGui.QPainter) -> None:
        """ Отрисовка _всех_ точек """

        painter.setBrush(self.point_brush)
        painter.setBackgroundMode(QtCore.Qt.OpaqueMode)

        # Рисуем точки
        for point_name, point in self.points.items():
            painter.drawEllipse(point, self.point_radius, self.point_radius)
            self.draw_label(painter, point, point_name)

    def draw_label(
            self, painter: QtGui.QPainter, point: QtCore.QPointF, label: str
    ) -> None:
        """ Отрисовка надписи """

        painter.drawText(
            QtCore.QPointF(
                point.x() + self.label_offset_x,
                point.y() + self.label_offset_y
            ),
            label
        )

    def update_pixmap(self) -> None:
        """ Метод, реализовано рисование на "полотне" (self.pixmap) """
        raise NotImplementedError

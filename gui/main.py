# coding: utf-8

import sys

from PyQt5 import QtWidgets

from gui.main_window import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()

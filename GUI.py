import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from InputHandler import get_device_list

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.combo_box = QtWidgets.QComboBox() 
        self.populate_combo_box()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.combo_box) 

    def populate_combo_box(self):
        device_list = get_device_list()
        for device in device_list:
            self.combo_box.addItem(device['product_name'])

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1280, 720)
    widget.show()

    sys.exit(app.exec())
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from InputHandler import get_device_list, get_device_info

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.window = QtWidgets.QTabWidget()

        # Main Tab
        self.tab_main = QtWidgets.QWidget()
        self.window.addTab(self.tab_main, "Main")

        # Devices Tab
        self.tab_devices = QtWidgets.QWidget()
        self.window.addTab(self.tab_devices, "Devices")        

        self.combo_box = QtWidgets.QComboBox(self.tab_main)
        self.populate_combo_box()
        self.select_button = QtWidgets.QPushButton("Select", self.tab_main)
        self.select_button.clicked.connect(self.selected_device)
        self.layout_Devices = QtWidgets.QHBoxLayout(self.tab_main)
        self.layout_Devices.addWidget(self.combo_box)
        self.layout_Devices.addWidget(self.select_button)
        self.tab_devices.setLayout(self.layout_Devices)

        # Widget to display selected device info
        self.device_info_label = QtWidgets.QLabel(self.tab_devices)
        self.device_info_label.setText("Selected Device Info:")
        self.device_info_text = QtWidgets.QTextEdit(self.tab_devices)
        self.device_info_text.setReadOnly(True)
        self.layout_device_info = QtWidgets.QVBoxLayout()
        self.layout_device_info.addWidget(self.device_info_label)
        self.layout_device_info.addWidget(self.device_info_text)
        self.layout_Devices.addLayout(self.layout_device_info)

        # Debug Tab
        self.tab_debug = QtWidgets.QWidget()
        self.window.addTab(self.tab_debug, "Debug")

        # Terminal for debug info
        self.debug_terminal = QtWidgets.QTextEdit(self.tab_debug)
        self.debug_terminal.setReadOnly(True)
        self.layout_debug_terminal = QtWidgets.QVBoxLayout()
        self.layout_debug_terminal.addWidget(self.debug_terminal)
        self.tab_debug.setLayout(self.layout_debug_terminal)

        # Top text before tabs
        self.selected_device_label = QtWidgets.QLabel(self)
        self.selected_device_label.setText("Selected device: None")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.selected_device_label)
        layout.addWidget(self.window)

    def populate_combo_box(self):
        device_list = get_device_list()
        for device in device_list:
            self.combo_box.addItem(get_device_info(device).get('product_name'))

    def selected_device(self):
        selected_index = self.combo_box.currentIndex()
        device_info = get_device_info(get_device_list()[selected_index])
        device_info_text = ""
        
        for key, value in device_info.items():
            device_info_text += f"{key}: {value}\n"          
        
        self.device_info_text.setPlainText(device_info_text)
        self.selected_device_label.setText("Selected device: "+device_info.get('product_name'))
        self.debug(f"Selected device: {device_info.get('product_name')}")        
        
    def debug(self, string):
        self.debug_terminal.clear()
        self.debug_terminal.append(string)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1280, 720)
    widget.show()

    sys.exit(app.exec())

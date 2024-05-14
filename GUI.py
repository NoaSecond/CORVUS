import sys
from PySide6 import QtCore, QtWidgets, QtGui

import pygame
from time import sleep
from msvcrt import kbhit

class MyWidget(QtWidgets.QWidget):
    device = None
        
    pygame.init()
    pygame.joystick.init()
    
    def __init__(self):
        super().__init__()

        self.window = QtWidgets.QTabWidget()

        # Main Tab
        self.tab_main = QtWidgets.QWidget()
        self.window.addTab(self.tab_main, "Main")

        # Devices Tab
        self.tab_devices = QtWidgets.QWidget()
        self.window.addTab(self.tab_devices, "Devices")   
        self.layout_Devices = QtWidgets.QHBoxLayout(self.tab_main)     
        # ComboBox devices
        self.combo_box = QtWidgets.QComboBox(self.tab_main)
        for i in range(pygame.joystick.get_count()):
            self.combo_box.addItem(pygame.joystick.Joystick(i).get_name())
        self.layout_Devices.addWidget(self.combo_box)
        # Select button
        self.select_button = QtWidgets.QPushButton("Select", self.tab_main)
        self.select_button.clicked.connect(self.select_device)
        # Add to layout
        self.layout_Devices.addWidget(self.select_button)
        self.tab_devices.setLayout(self.layout_Devices)

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

    def select_device(self):
        selected_index = self.combo_box.currentIndex()
        self.device = pygame.joystick.Joystick(selected_index)
        self.selected_device_label.setText("Selected device: "+self.device.get_name())  
        self.debug(f"Selected device info:\n"+
        "name: "+self.device.get_name()+"\n"+
        "num_axes: "+str(self.device.get_numaxes())+"\n"+
        "num_buttons: "+str(self.device.get_numbuttons())+"\n"+
        "num_hats: "+str(self.device.get_numhats()))     
        self.add_device_inputs_to_main_tab()    
        
    def debug(self, string):
        self.debug_terminal.append(string)
        
    def add_device_inputs_to_main_tab(self):
        grid_buttons = QtWidgets.QGridLayout()
        grid_axis = QtWidgets.QGridLayout()
        grid_hats = QtWidgets.QGridLayout()
        
        for i in range(self.device.get_numbuttons()):
            label = QtWidgets.QLabel("Button " + str(i), self.tab_main)
            value_label = QtWidgets.QLabel("0", self.tab_main)
            grid_buttons.addWidget(label, i, 0)
            grid_buttons.addWidget(value_label, i, 1)
            self.buttons_labels.append(value_label)
            
        for i in range(self.device.get_numaxes()):
            label = QtWidgets.QLabel("Axis " + str(i), self.tab_main)
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.tab_main)
            slider.setMinimum(-100)
            slider.setMaximum(100)
            slider.setValue(0)
            value_label = QtWidgets.QLabel("0", self.tab_main)
            grid_axis.addWidget(label, i, 0)
            grid_axis.addWidget(slider, i, 1)
            grid_axis.addWidget(value_label, i, 2)
            self.axes_sliders.append((slider, value_label))
            
        for i in range(self.device.get_numhats()):
            label = QtWidgets.QLabel("Hat " + str(i), self.tab_main)
            value_label = QtWidgets.QLabel("0", self.tab_main)
            grid_hats.addWidget(label, i, 0)
            grid_hats.addWidget(value_label, i, 1)
            self.hats_labels.append(value_label)
            
        self.tab_main.layout = QtWidgets.QVBoxLayout()
        self.tab_main.layout.addLayout(grid_buttons)
        self.tab_main.layout.addLayout(grid_axis)
        self.tab_main.layout.addLayout(grid_hats)
        self.tab_main.setLayout(self.tab_main.layout)

    def update_values(self):
        while True:
            pygame.event.get()
            if self.device:
                for i in range(self.device.get_numbuttons()):
                    self.buttons_labels[i].setText(str(self.device.get_button(i)))
                
                for i in range(self.device.get_numaxes()):
                    value = self.device.get_axis(i)
                    self.axes_sliders[i][0].setValue(int(value * 100))
                    self.axes_sliders[i][1].setText(str(round(value, 2)))
                    
                for i in range(self.device.get_numhats()):
                    self.hats_labels[i].setText(str(self.device.get_hat(i)))
            QtWidgets.qApp.processEvents()
            QtCore.QThread.msleep(50)
            

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1280, 720)
    widget.show()

    sys.exit(app.exec())

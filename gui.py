import unreal
import sys
from functools import partial
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QColorDialog, QLabel, QVBoxLayout)
from PySide6.QtGui import QColor

if QApplication.instance():
    for win in (QApplication.allWindows()):
        if 'Toolbox Window' in win.objectName():
            win.destroy()
else:
    app = QApplication(sys.argv)

class UnrealToolWindow(QWidget):
    def __init__ (self, parent = None):
        super(UnrealToolWindow, self).__init__(parent)

        self.main_window = QMainWindow()
        self.main_window.setParent(self)

class ColorPickerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTile("Color Picker")
        self.setGeometry(100, 100, 300, 200)

        #Create widget

        #Button to open 

        #



window = QWidget()
window.setObjectName("Toolbox Window")
window.setWindowTitle("Unreal Toolbox")
window.show()
unreal.parent_external_window_to_slate(window.winId())


# edit.setAcceptDrops(True) <-- Drag and dropper
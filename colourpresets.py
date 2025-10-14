import unreal
import sys
from functools import partial
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

# Create buttons
class ColorPresets(QWidget):
    def __init__ (self, parent = None):
        super(ColorPresets, self).__init__(parent)

        self.main_window = QMainWindow()
        self.main_window.setParent(self)
        self.main_window.setFixedSize(QSize(400,300))

        self.button = QPushButton("Button")
        self.button.setCheckable(True)

        self.button.clicked.connect(self.buttonClicked)

        self.main_window.setCentralWidget(self.button)

    def buttonClicked(Self, checked):
        unreal.log ('BUTTON CLICKED')
        unreal.log ("Checked: " + str(checked))
        pass

def launchWindow():
    if QApplication.instance():
        for win in (QApplication.allWindows()):
            if 'toolWindow' in win.objectName():
                win.destroy()
    else:
        app = QApplication(sys.argv)
 
    ColorPresets.window = ColorPresets()
    ColorPresets.window.setObjectName("toolWindow")
    ColorPresets.window.setWindowTitle("Colour Preset")
    ColorPresets.window.show()
    unreal.parent_external_window_to_slate(ColorPresets.window.winId())
launchWindow()

# Assign colours to buttons



# Button functionality (Hex code copied upon push)
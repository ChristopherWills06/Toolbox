import unreal
import sys
from functools import partial
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMainWindow, QColorDialog, QVBoxLayout
)
from PySide6.QtGui import QColor
 
 
class ColorPicker(QWidget):
    def __init__(self, parent=None):
        super(ColorPicker, self).__init__(parent)
 
        # Main Window Creation
        self.main_window = QMainWindow()
        self.main_window.setParent(self)
        self.main_window.setFixedSize(QSize(400, 300))
        self.main_window.setWindowTitle("Colour Picker")
 
        # Widget Container
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)
 
        # Button Layout
        layout = QVBoxLayout(central_widget)
 
        # Colour Picker Button
        self.button = QPushButton("Pick a Colour")
        self.button.setCheckable(False)
        self.button.setStyleSheet("background-color: cyan; font-weight: bold; font-size: 14px;")
 
        # Button to Picker Connection
        self.button.clicked.connect(self.open_color_picker)
 
        layout.addWidget(self.button)
 
    def open_color_picker(self):
        """Opens a QColorDialog and updates button color"""
        color = QColorDialog.getColor(QColor("cyan"), self, "Select a Color")
 
        if color.isValid():
            # Apply Chosen Colour
            css = f"background-color: {color.name()}; font-weight: bold; font-size: 14px;"
            self.button.setStyleSheet(css)
 
            # Log Colour to Unreal
            unreal.log(f"Selected Color: {color.name()}")
        else:
            unreal.log("Color selection canceled.")
 
 
def launchWindow():
    # Destroy old window if already open
    if QApplication.instance():
        for win in QApplication.allWindows():
            if 'toolWindow' in win.objectName():
                win.close()
                win.deleteLater()
    else:
        app = QApplication(sys.argv)
 
    # Create and show the window
    ColorPicker.window = ColorPicker()
    ColorPicker.window.setObjectName("toolWindow")
    ColorPicker.window.setWindowTitle("Color Preset")
    ColorPicker.window.show()
 
    # Attach to Unreal's main window
    unreal.parent_external_window_to_slate(ColorPicker.window.winId())
 
 
# Run it
launchWindow()
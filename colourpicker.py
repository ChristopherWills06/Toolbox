import unreal
import sys
from functools import partial
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication, QColor, QCursor, QClipboard
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMainWindow, QColorDialog, QVBoxLayout, QLabel, QVBoxLayout
)

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
        self.button.setStyleSheet("background-color: red; font-weight: bold; font-size: 14px;")
 
        self.btn2 = QPushButton("Pick a Colour")
        self.btn2.setCheckable(False)
        self.btn2.setStyleSheet("background-color: orange; font-weight: bold; font-size: 14px;")

        # Button to Picker Connection
        self.button.clicked.connect(self.open_color_picker)
        self.btn2.clicked.connect(self.open_color_picker)

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

######################################################
######################################################

class Eyedropper(QWidget):
    def __init__(self):
        super().__init__()
 
        self.setWindowTitle("Eyedropper Tool")
        self.resize(250, 150)
        self.pick_btn = QPushButton("Pick Color")
        self.pick_btn.clicked.connect(self.activate_picker)

        self.copy_button = QPushButton("📎")
        self.copy_button.clicked.connect(self.copy_label)
 
        self.color_label = QLabel("Click 'Pick Color' to sample.")
        self.color_label.setAlignment(Qt.AlignCenter)
       
        layout = QVBoxLayout()
        layout.addWidget(self.pick_btn)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.color_label)
        self.setLayout(layout)
 
        self.picking = False
 
    def activate_picker(self):
        """Enable color picking mode."""
        self.picking = True
        self.color_label.setText("Click anywhere to pick color…")
        self.setWindowOpacity(0.6)
        QApplication.setOverrideCursor(Qt.CrossCursor)
        self.grabMouse()
 
    def mousePressEvent(self, event):
        """Triggered when user clicks anywhere on screen."""
        if not self.picking:
            return
 
        # Capture the mouse position
        pos = QCursor.pos()
 
        # Grab entire screen and read pixel color
        screen = QGuiApplication.primaryScreen()
        pixmap = screen.grabWindow(0, pos.x(), pos.y(), 1, 1)
        image = pixmap.toImage()
        color = QColor(image.pixel(0, 0))
 
        self.show_color(color)
 
        # Reset state
        self.releaseMouse()
        QApplication.restoreOverrideCursor()
        self.setWindowOpacity(1.0)
        self.picking = False
 
    def show_color(self, color: QColor):
        """Display the picked color and its hex/RGB values."""
        rgb_text = f"RGB: {color.red()}, {color.green()}, {color.blue()}"
        hex_text = f"HEX: {color.name().upper()}"
        self.color_label.setText(f"{rgb_text}\n{hex_text}")
        self.color_label.setStyleSheet(f"background-color: {color.name()}; color: white;")   

    def copy_label(self):
        self = self.label.text
        if text.strip():
            clipboard = QApplication.clipboard()
            clipboard.setText(text,QClipboard.Clipboard)
            print(f"Copied to clipboard: {text}")

######################################################
######################################################
 
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

    Eyedropper.window = Eyedropper()
    Eyedropper.window.setObjectName("toolWindow")
    Eyedropper.window.setWindowTitle("Color Preset")
    Eyedropper.window.show()
 
    # Attach to Unreal's main window
    unreal.parent_external_window_to_slate(ColorPicker.window.winId())
    unreal.parent_external_window_to_slate(Eyedropper.window.winId())
 
# Run it
launchWindow()
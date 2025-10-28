import unreal
import sys
from functools import partial
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication, QColor, QCursor, QClipboard, QPainter
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

        self.setLayout(layout)

        # Button to Picker Connection
        self.button.clicked.connect(self.open_color_picker)
        self.btn2.clicked.connect(self.open_color_picker)

        layout.addWidget(self.button)
        layout.addWidget(self.btn2)
 
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

COLOURBLIND_MATRICES = {
    "Protanopia": [
        [0.56667, 0.43333, 0.0],
        [0.55833, 0.44167, 0.0],
        [0.0,      0.24167, 0.75833]
    ],
    "Deuteranopia": [
        [0.625, 0.375, 0.0],
        [0.7,   0.3,   0.0],
        [0.0,   0.3,   0.7]
    ],
    "Tritanopia": [
        [0.95,  0.05,  0.0],
        [0.0,   0.43333, 0.56667],
        [0.0,   0.475, 0.525]
    ]
}
        
def simulate_colour_blind(rgb_tuple, matrix):
    #apply matrice to colour
    r, g, b = [c /255.0 for c in rgb_tuple]
    r_new = r * matrix[0][0] + g * matrix[0][1] + b * matrix[0][2]
    g_new = r * matrix[1][0] + g * matrix[1][1] + b * matrix[1][2]
    b_new = r * matrix[2][0] + g * matrix[2][1] + b * matrix[2][2]
    return tuple(max(0, min(255, int(c * 255))) for c in (r_new, b_new, g_new))

class ColourBlindChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Colourblind Checker")
        self.resize(400,300)

        self.original_colour = QColor(255, 0, 0)

        layout = QVBoxLayout()
        self.label = QLabel("True Colour")

        self.pick_button = QPushButton("Choose Colour")
        self.pick_button.clicked.connect(self.choose_colour)

        layout.addWidget(self.label)
        layout.addWidget(self.pick_button)

        self.setLayout(layout)

    def choose_colour(self):
        colour = QColorDialog.getColor(self.original_colour, self, "Select Colour")
        if colour.isValid():
            self.original_colour = colour
            self.update()

    def simulate_colours(self):
        painter = QPainter(self)

        #original colour
        painter.fillRect(20, 60, 100, 100, self.original_colour)
        painter.drawText(20, 180, "Original")

        #simulated colour boxes
        x_offset = 140
        for name, matrix in COLOURBLIND_MATRICES.items():
            sim_rgb = simulate_colour_blind(
                {self.original_colour.red(),
                self.original_colour.green(),
                self.original_colour.blue()},
                matrix
            )
            painter.fillRect(x_offset, 60, 100, 100, QColor(*sim_rgb))
            painter.drawText(x_offset, 180, name)
            x_offset += 120

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
    Eyedropper.window.setWindowTitle("Eyedropper")
    Eyedropper.window.show()

    ColourBlindChecker.window = ColourBlindChecker()
    ColourBlindChecker.window.setObjectName("toolWindow")
    ColourBlindChecker.window.setWindowTitle("Colourblind Checker")
    ColourBlindChecker.window.show()
 
    # Attach to Unreal's main window
    unreal.parent_external_window_to_slate(ColorPicker.window.winId())
    unreal.parent_external_window_to_slate(Eyedropper.window.winId())
    unreal.parent_external_window_to_slate(ColourBlindChecker.window.winId())
 
# Run it
launchWindow()
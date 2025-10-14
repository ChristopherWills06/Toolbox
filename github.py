import unreal
import sys
from functools import partial
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QSlider,QVBoxLayout, QLabel
 
class UnrealToolWindow(QWidget):
    def __init__ (self, parent = None):
       
        # Run the Init of Qwidget <--- Parent
        super(UnrealToolWindow, self).__init__(parent)
 
        # Setting up the properties of my UnrealToolWindow
        self.main_window = QMainWindow()
        self.main_window.setParent(self)
        self.main_window.setFixedSize(QSize(400,300))
 
        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        # Create a Click Event that when the button is clicked it will call the function
        # ButtonClicked()
        self.button.clicked.connect(self.buttonClicked)
 
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(50)
        self.slider.setSliderPosition(25)
        self.slider.valueChanged.connect(self.sliderChanged)
 
        self.label = QLabel()
        self.label.setText("0")
 
        ##################################
 
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
 
        container = QWidget()
        container.setLayout(layout)
 
        self.main_window.setCentralWidget(container)
 
    def sliderChanged(self,value):
        unreal.log("Slider was moved to: " + str(value))
        self.label.setText(str(value))
 
    def buttonClicked(self, checked):
        unreal.log ('BUTTON CLICKED')
        unreal.log ("Checked: " + str(checked) )
 
        if checked:
            self.button.setText ("Button was already Pressed!")
        else:
            self.button.setText ("Press Again!")
 
 
def launchWindow():
    if QApplication.instance():
        for win in (QApplication.allWindows()):
            if 'toolWindow' in win.objectName():
                win.destroy()
    else:
        app = QApplication(sys.argv)
 
    UnrealToolWindow.window = UnrealToolWindow()
    UnrealToolWindow.window.setObjectName("toolWindow")
    UnrealToolWindow.window.setWindowTitle("Button Tool")
    UnrealToolWindow.window.show()
    unreal.parent_external_window_to_slate(UnrealToolWindow.window.winId())
 
launchWindow()
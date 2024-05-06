import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QStatusBar,
    QToolBar,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        #This is how to dynamically add more tools. Simply just added the tool name as the key and the function name as the data and it will be added
        self.dict_of_menu_options = {}
        self.dict_of_toolbar_options={}

        #The image goes here
        self.image_label = QLabel("No Image Loaded")
        #This is for the scaling of an image
        self.scale_factor = 1.0

        self.setWindowTitle("Basic Image Manipulator")
        #Uncomment if you want to load an image at startup
        # self.load_image()
        #
        self.add_load_image_to_menu()
        self.create_zoom_buttons()

        #Add new tools must be functions must be added before these functions. These functions create the menus
        self.createMenuBar()
        self.createToolBar()

        #Can change this to tell you which tool you have selected? Currently does nothing important
        self._createStatusBar()

        # Create a central widget and set the layout on it
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.image_label)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)     
        
    def createMenuBar(self):
        """
        Loops through the dictionary of menu options and adds them to the main menu.
        """
        menu = self.menuBar().addMenu("&Menu")
        self.create_menu_tool("&Exit", self.close)
        for item, function in self.dict_of_menu_options.items():
            menu.addAction(item, function)

    def createToolBar(self):
        """
        Loops through the dictionary of toolbar options and adds them to the toolbar.
        """
        tools = QToolBar()
        self.create_toolbar_tool("Exit", self.close)
        for item, function in self.dict_of_toolbar_options.items():
            tools.addAction(item, function)
        self.addToolBar(tools)

    def _createStatusBar(self):
        """
        Currently does nothing.
        """
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

    def create_menu_tool(self, tool, function):
        """
        Helper function to just add a tool to the menu
        """
        self.dict_of_menu_options[tool] = function

    def create_toolbar_tool(self, tool, function):
        """
        Helper function to just add a tool to the toolbar
        """
        self.dict_of_toolbar_options[tool] = function

    def add_load_image_to_menu(self):
        """
        Adds load image to the menu
        """
        self.create_menu_tool("&Load_Image", self.load_image)

    def load_image(self):
        """
        This loads images with a certain file name tag. This is to prevent crashing the program.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.JPG *.bmp)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(selected_file)
            if not pixmap.isNull():
                self.original_pixmap = pixmap
                self.update_image()
            else:
                self.image_label.setText("Invalid Image")

    def update_image(self):
        """
        This function currently just updates the image based on just the zoom in and out. Can be changed to be more of a general function
        """
        scaled_width = int(self.original_pixmap.width() * self.scale_factor)
        #scaled_height = int(self.original_pixmap.height() * self.scale_factor)
        scaled_pixmap = self.original_pixmap.scaledToWidth(scaled_width)
        self.image_label.setPixmap(scaled_pixmap)

    def zoom_in(self):
        """
        Zooms in on an image
        """
        self.scale_factor *= 1.1
        self.update_image()

    def zoom_out(self):
        """
        Zooms out on an image
        """
        self.scale_factor *= 0.9
        self.update_image()
    
    
    def create_zoom_buttons(self):
        """
        Adds the zooming functionality to the toolbar
        """
        self.dict_of_toolbar_options["Zoom In"] = self.zoom_in
        self.dict_of_toolbar_options["Zoom Out"] = self.zoom_out


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
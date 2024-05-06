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

        self.dict_of_menu_options = {}
        self.dict_of_toolbar_options={}
        self.image_label = QLabel("No Image Loaded")
        self.scale_factor = 1.0

        self.setWindowTitle("QMainWindow")

        self.load_image()
        self.add_load_image_to_menu()

        self.create_zoom_buttons()

        self.create_menuBar()

        self.createToolBar()
        self._createStatusBar()

        # Create a central widget and set the layout on it
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.image_label)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def populate_menu(self):
        menu = self.menuBar().addMenu("&Menu")
        self.create_menu_tool("&Exit", self.close)
        for item, function in self.dict_of_menu_options.items():
            menu.addAction(item, function)
        
    def create_menuBar(self):
        self.populate_menu()

    def createToolBar(self):
        tools = QToolBar()
        self.create_toolbar_tool("Exit", self.close)
        for item, function in self.dict_of_toolbar_options.items():
            tools.addAction(item, function)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

    def create_menu_tool(self, tool, function):
        self.dict_of_menu_options[tool] = function

    def create_toolbar_tool(self, tool, function):
        self.dict_of_toolbar_options[tool] = function

    def add_load_image_to_menu(self):
        self.create_menu_tool("&Load_Image", self.load_image)

    def load_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
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
        scaled_width = int(self.original_pixmap.width() * self.scale_factor)
        #scaled_height = int(self.original_pixmap.height() * self.scale_factor)
        scaled_pixmap = self.original_pixmap.scaledToWidth(scaled_width)
        self.image_label.setPixmap(scaled_pixmap)

    def zoom_in(self):
        self.scale_factor *= 1.1
        self.update_image()

    def zoom_out(self):
        self.scale_factor *= 0.9
        self.update_image()
    
    
    def create_zoom_buttons(self):
        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.zoom_in)
        self.dict_of_toolbar_options["Zoom In"] = self.zoom_in
        
        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.zoom_out)
        self.dict_of_toolbar_options["Zoom Out"] = self.zoom_out


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
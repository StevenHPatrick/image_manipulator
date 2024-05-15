import sys

from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget, QStatusBar, QToolBar, QFileDialog,
    QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QInputDialog
)
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QAction, QFont
from PySide6.QtCore import Qt, QRect, QPointF
from filters import *


class Window(QMainWindow):

    def __init__(self):
        super().__init__(parent=None)
        # This is how to dynamically add more tools. Simply just added the tool name as the key
        # and the function name as the data and it will be added
        self.dict_of_menu_options = {}
        self.dict_of_toolbar_options = {}
        self.pixmap = None
        self.loaded_pixmap = None


        self.crop_start = None
        self.crop_end = None
        self.cropping = False

        # The image goes here
        self.image_label = QLabel("No Image Loaded")
        # This is for the scaling of an image
        self.scale_factor = 1.0

        self.setWindowTitle("Basic Image Manipulator")
        # Uncomment if you want to load an image at startup
        # self.load_image()
        #
        self.open_image_button()
        self.add_load_image_to_menu()
        self.create_zoom_buttons()
        self.create_crop_tools()
        self.create_add_text_button()
        self.create_save_image_button()

        # Add new tools must be functions must be added before these functions. These functions create the menus
        self.create_menu_bar()
        self.create_filter_menu()
        self.create_tool_bar()

        # Tells you which tool is selected / status of the app
        self.create_status_bar()

        # Create a central widget and set the layout on it
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.image_label)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Variables to track text position and movement
        self.text_position = QPointF(0, 0)
        self.is_text_selected = False
        self.offset = QPointF()

        # Enable mouse tracking for cropping
        self.image_label.setMouseTracking(True)
        self.image_label.mousePressEvent = self.start_crop
        self.image_label.mouseMoveEvent = self.drawing_crop
        self.image_label.mouseReleaseEvent = self.perform_crop

        # Enable mouse tracking for moving text
        # self.image_label.mouseDoubleClickEvent = self.select_text
        # self.image_label.mouseMoveEvent = self.move_text
        # self.image_label.mouseReleaseEvent = self.release_text


    def create_menu_bar(self):
        """
        Loops through the dictionary of menu options and adds them to the main menu.
        """
        menu = self.menuBar().addMenu("&Menu")
        self.create_menu_tool("&Exit", self.close)
        for item, function in self.dict_of_menu_options.items():
            menu.addAction(item, function)

    def create_tool_bar(self):
        """
        Loops through the dictionary of toolbar options and adds them to the toolbar.
        """
        tools = QToolBar()
        self.create_toolbar_tool("Exit", self.close)
        for item, function in self.dict_of_toolbar_options.items():
            tools.addAction(item, function)
        self.addToolBar(tools)

    def create_status_bar(self):
        """
        Creates the status bar
        """
        self.status = QStatusBar()
        self.update_status("Hello!")

    def update_status(self, message):
        """
        A helper function to update the status bar for various functions
        """
        self.status.showMessage(message)
        self.setStatusBar(self.status)

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
        self.create_menu_tool("&Load Image", self.load_image)

    def load_image(self):
        """
        This loads images with a certain file name tag. This is to prevent crashing the program.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.JPG *.bmp)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(selected_file)
            if not pixmap.isNull():
                self.pixmap = pixmap
                self.loaded_pixmap = pixmap.copy()  # Saving a copy for reverting
                self.update_image()
                self.update_status("Opened " + selected_file)
            else:
                self.image_label.setText("Invalid Image")

    def update_image(self):
        """
        This function currently just updates the image based on just the zoom in and out.
        Can be changed to be more of a general function
        """
        scaled_width = int(self.pixmap.width() * self.scale_factor)
        # scaled_height = int(self.pixmap.height() * self.scale_factor)
        scaled_pixmap = self.pixmap.scaledToWidth(scaled_width)
        self.image_label.setPixmap(scaled_pixmap)

    def zoom_in(self):
        """
        Zooms in on an image
        """
        self.scale_factor *= 1.1
        self.update_image()
        self.update_status("Zoomed In")

    def zoom_out(self):
        """
        Zooms out on an image
        """
        self.scale_factor *= 0.9
        self.update_image()
        self.update_status("Zoomed Out")

    def create_zoom_buttons(self):
        """
        Adds the zooming functionality to the toolbar
        """
        self.dict_of_toolbar_options["Zoom In"] = self.zoom_in
        self.dict_of_toolbar_options["Zoom Out"] = self.zoom_out

    def open_image_button(self):
        self.dict_of_toolbar_options["Open image"] = self.load_image

    def toggle_crop_mode(self):
        self.cropping = not self.cropping
        status_message = "Cropping Mode On" if self.cropping else "Cropping Mode Off"
        self.update_status(status_message)

    def crop_image(self):
        """
        Crop the image based on user selection.
        """
        if self.pixmap and self.crop_start and self.crop_end:
            rect = QRect(self.crop_start, self.crop_end)
            cropped_pixmap = self.pixmap.copy(rect)
            self.pixmap = cropped_pixmap
            self.update_image()
            self.crop_start = None
            self.crop_end = None
            self.update_status("Crop applied.")

    def revert(self):
        """
        Revert to the original image.
        """
        if self.loaded_pixmap:
            self.pixmap = self.loaded_pixmap.copy()
            self.scale_factor = 1.0  # Reset the scale factor
            self.update_image()
            self.update_status("Changes reverted.")

    def start_crop(self, event):
        if self.cropping and self.pixmap:
            self.crop_start = event.position().toPoint()
            self.update_status("Crop Started")

    def drawing_crop(self, event):
        if self.cropping and self.pixmap and self.crop_start:
            self.temp_pixmap = self.pixmap.copy()
            painter = QPainter(self.temp_pixmap)
            pen = QPen(QColor(255, 0, 0), 2, Qt.DashLine)
            painter.setPen(pen)
            rect = QRect(self.crop_start, event.position().toPoint())
            painter.drawRect(rect)
            self.image_label.setPixmap(self.temp_pixmap)
            self.crop_end = event.position().toPoint()

    def perform_crop(self, event):
        if self.cropping and self.pixmap and self.crop_start and self.crop_end:
            rect = QRect(self.crop_start, self.crop_end)
            cropped_pixmap = self.pixmap.copy(rect)
            self.pixmap = cropped_pixmap
            self.update_image()
            self.crop_start = None
            self.crop_end = None
            self.update_status("Crop applied.")
            self.cropping = False

    def create_crop_tools(self):
        self.create_toolbar_tool("Crop", self.toggle_crop_mode)
        self.create_toolbar_tool("Revert", self.revert)

    def save_image(self):
        """
        Saves the current image to a file.
        """
        if self.pixmap:
            file_dialog = QFileDialog(self)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
            file_dialog.setDefaultSuffix("png")
            if file_dialog.exec():
                save_path = file_dialog.selectedFiles()[0]
                if self.pixmap.save(save_path):
                    self.update_status(f"Image saved to {save_path}")
                else:
                    self.update_status("Failed to save image")

    def create_save_image_button(self):
        self.create_toolbar_tool("Save image", self.save_image)

    def create_filter_menu(self):
        """
        Create a submenu for filters.
        """
        filter_menu = QMenu("Filters", self)

        grayscale_action = QAction("Grayscale", self)
        grayscale_action.triggered.connect(self.apply_grayscale)
        filter_menu.addAction(grayscale_action)

        sepia_action = QAction("Sepia", self)
        sepia_action.triggered.connect(self.apply_sepia)
        filter_menu.addAction(sepia_action)

        invert_action = QAction("Invert", self)
        invert_action.triggered.connect(self.apply_invert)
        filter_menu.addAction(invert_action)

        blur_action = QAction("Blur", self)
        blur_action.triggered.connect(self.apply_blur)
        filter_menu.addAction(blur_action)

        sharpen_action = QAction("Sharpen", self)
        sharpen_action.triggered.connect(self.apply_sharpen)
        filter_menu.addAction(sharpen_action)

        self.menuBar().addMenu(filter_menu)



    def apply_grayscale(self):
        if self.pixmap:
            self.pixmap = apply_grayscale(self.pixmap)
            self.update_image()
            self.update_status("Applied Grayscale filter")

    def apply_sepia(self):
        if self.pixmap:
            self.pixmap = apply_sepia(self.pixmap)
            self.update_image()
            self.update_status("Applied Sepia filter")

    def apply_invert(self):
        if self.pixmap:
            self.pixmap = apply_invert(self.pixmap)
            self.update_image()
            self.update_status("Applied Invert filter")

    def apply_blur(self):
        """
        Apply a blur filter to the image.
        """
        if self.pixmap:
            self.pixmap = apply_blur(self.pixmap)
            self.update_image()
            self.update_status("Applied Blur filter")

    def apply_sharpen(self):
        """
        Apply a sharpen filter to the image.
        """
        if self.pixmap:
            self.pixmap = apply_sharpen(self.pixmap)
            self.update_image()
            self.update_status("Applied Sharpen filter")

    def create_add_text_button(self):
        """
        Create a button to add text to the image.
        """
        self.create_toolbar_tool("Add Text", self.add_text_to_image)

    def add_text_to_image(self):
        """
        Open a dialog to add text to the image.
        """
        text, ok = QInputDialog.getText(self, "Add Text", "Enter the text:")
        try:
            if ok and text:
                painter = QPainter(self.pixmap)

                font = QFont("Arial", 20)
                painter.setFont(font)
                painter.setPen(QColor(Qt.white))
                text_rect = painter.boundingRect(self.image_label.geometry(), Qt.AlignCenter, text)

                painter.drawText(text_rect, Qt.AlignCenter, text)
                painter.end()

                self.update_image()
                self.update_status("Text added to image.")
        except Exception as e:
            print("An error occurred:", e)
            self.update_status("Failed to add text.")




if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

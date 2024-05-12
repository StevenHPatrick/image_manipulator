import sys
from math import cos, sin
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget, QStatusBar, QToolBar, QFileDialog,
    QVBoxLayout, QHBoxLayout, QPushButton, QMenu
)
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QTimer

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.dict_of_menu_options = {}
        self.dict_of_toolbar_options = {}

      
        self.image_label = QLabel("No Image Loaded")
        self.scale_factor = 1.0
        self.original_pixmap = None
        self.loaded_pixmap = None  
        self.crop_start = None
        self.crop_end = None
        self.temp_pixmap = None
        self.spiral_timer = QTimer()
        self.spiral_counter = 0
        self.spiral_effect_enabled = False

      
        self.setWindowTitle("Basic Image Manipulator")
        self.setup_toolbar()
        self.setup_menu_bar()
        self.setup_status_bar()

        
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.image_label)
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # Enable mouse tracking for cropping
        self.image_label.setMouseTracking(True)
        self.image_label.mousePressEvent = self.start_crop
        self.image_label.mouseMoveEvent = self.drawing_crop
        self.image_label.mouseReleaseEvent = self.perform_crop

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.add_toolbar_button("Open Image", self.load_image, toolbar)
        self.add_toolbar_button("Zoom In", self.zoom_in, toolbar)
        self.add_toolbar_button("Zoom Out", self.zoom_out, toolbar)
        self.add_toolbar_button("Crop", self.perform_crop, toolbar)
        #self.add_toolbar_button("Spiral", self.apply_spiral_effect, toolbar)
        self.add_toolbar_button("Revert", self.revert_changes, toolbar)
        self.add_toolbar_button("Save Image", self.save_image, toolbar)
        self.addToolBar(toolbar)

    def add_toolbar_button(self, label, function, toolbar):
        button = QPushButton(label)
        button.clicked.connect(function)
        toolbar.addWidget(button)

    def setup_menu_bar(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def load_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.JPG *.bmp)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            pixmap = QPixmap(selected_file)
            if not pixmap.isNull():
                self.original_pixmap = pixmap
                self.loaded_pixmap = pixmap.copy()  # Store the original loaded image for reverting
                self.update_image()
                self.status_bar.showMessage("Opened " + selected_file)
            else:
                self.image_label.setText("Invalid Image")

    def update_image(self):
        if self.original_pixmap:
            scaled_width = int(self.original_pixmap.width() * self.scale_factor)
            scaled_pixmap = self.original_pixmap.scaledToWidth(scaled_width)
            self.image_label.setPixmap(scaled_pixmap)

    def zoom_in(self):
        self.scale_factor *= 1.1
        self.update_image()

    def zoom_out(self):
        self.scale_factor *= 0.9
        self.update_image()

    def revert_changes(self):
        if self.loaded_pixmap:
            self.original_pixmap = self.loaded_pixmap.copy()
            self.scale_factor = 1.0  # Reset the scale factor
            self.update_image()
            self.status_bar.showMessage("Changes reverted.")

    def start_crop(self, event):
        if self.original_pixmap:
            self.crop_start = event.pos()

    def drawing_crop(self, event):
        if self.original_pixmap and self.crop_start:
            self.temp_pixmap = self.original_pixmap.copy()
            painter = QPainter(self.temp_pixmap)
            pen = QPen(QColor(255, 0, 0), 2, Qt.DashLine)
            painter.setPen(pen)
            rect = QRect(self.crop_start, event.pos())
            painter.drawRect(rect)
            self.image_label.setPixmap(self.temp_pixmap)
            self.crop_end = event.pos()

    def perform_crop(self, event):
        if self.original_pixmap and self.crop_start and self.crop_end:
            rect = QRect(self.crop_start, self.crop_end)
            cropped_pixmap = self.original_pixmap.copy(rect)
            self.original_pixmap = cropped_pixmap
            self.update_image()
            self.crop_start = None
            self.crop_end = None
            self.status_bar.showMessage("Crop applied.")

    def save_image(self):
        if self.original_pixmap:
            file_dialog = QFileDialog(self)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setDefaultSuffix("png")
            file_dialog.setNameFilter("PNG files (*.png)")
            if file_dialog.exec():
                selected_file = file_dialog.selectedFiles()[0]
                self.original_pixmap.save(selected_file)
                self.status_bar.showMessage("Image Saved As " + selected_file)
    
    # def apply_spiral_effect(self):
    #     if not self.spiral_effect_enabled:
    #         self.spiral_timer.timeout.connect(self.spiral_image)
    #         self.spiral_timer.start(100)  # Change the delay as needed to control the speed of the effect
    #         self.spiral_effect_enabled = True
    #     else:
    #         self.spiral_timer.stop()
    #         self.spiral_effect_enabled = False

    # def spiral_image(self):
    #     if self.original_pixmap:
    #         width, height = self.original_pixmap.width(), self.original_pixmap.height()
    #         spiral_factor = 0.1  # Adjust this value to control the intensity of the spiral effect
    #         spiral_image = QPixmap(width, height)
    #         spiral_image.fill(Qt.transparent)
    #         painter = QPainter(spiral_image)
    #         center_x, center_y = width / 2, height / 2
    #         for y in range(height):
    #             for x in range(width):
    #                 angle = (x - center_x + y - center_y) * spiral_factor
    #                 new_x = int(center_x + (x - center_x) * cos(angle) - (y - center_y) * sin(angle))
    #                 new_y = int(center_y + (x - center_x) * sin(angle) + (y - center_y) * cos(angle))
    #                 if 0 <= new_x < width and 0 <= new_y < height:
    #                     color = self.original_pixmap.toImage().pixel(x, y)
    #                     painter.setPen(QColor(color))
    #                     painter.drawPoint(new_x, new_y)
    #         painter.end()
    #         self.image_label.setPixmap(spiral_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

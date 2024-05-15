import cv2
import numpy as np
from PySide6.QtGui import QPixmap, QImage, QColor


def apply_grayscale(pixmap):
    image = pixmap.toImage()
    for x in range(image.width()):
        for y in range(image.height()):
            color = image.pixelColor(x, y)
            gray = int(0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue())
            gray_color = QColor(gray, gray, gray)
            image.setPixelColor(x, y, gray_color)
    return QPixmap.fromImage(image)


def apply_sepia(pixmap):
    image = pixmap.toImage()
    for x in range(image.width()):
        for y in range(image.height()):
            pixel_color = QColor(image.pixelColor(x, y))
            sepia_r = min(255, int(0.393 * pixel_color.red() + 0.769 * pixel_color.green() + 0.189 * pixel_color.blue()))
            sepia_g = min(255, int(0.349 * pixel_color.red() + 0.686 * pixel_color.green() + 0.168 * pixel_color.blue()))
            sepia_b = min(255, int(0.272 * pixel_color.red() + 0.534 * pixel_color.green() + 0.131 * pixel_color.blue()))
            sepia_color = QColor(sepia_r, sepia_g, sepia_b)
            image.setPixelColor(x, y, sepia_color)
    return QPixmap.fromImage(image)


def apply_invert(pixmap):
    image = pixmap.toImage()
    for x in range(image.width()):
        for y in range(image.height()):
            color = image.pixelColor(x, y)
            inverted_color = QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())
            image.setPixelColor(x, y, inverted_color)
    return QPixmap.fromImage(image)


def apply_blur(pixmap):
    """
    Apply a blur filter to the image using OpenCV.
    """
    # Convert QPixmap to QImage
    img = pixmap.toImage().convertToFormat(QImage.Format_RGB888)
    w, h = img.width(), img.height()

    # Get image data as numpy array
    ptr = img.bits()
    arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 3))

    # Apply blur filter using OpenCV
    blurred_arr = cv2.GaussianBlur(arr, (15, 15), 0)

    # Convert back to QImage
    qimg = QImage(blurred_arr.data, w, h, 3 * w, QImage.Format_RGB888)

    # Convert QImage back to QPixmap
    pixmap_blurred = QPixmap.fromImage(qimg)

    return pixmap_blurred

def apply_sharpen(pixmap):
    """
    Apply a sharpen filter to the image using OpenCV.
    """
    # Convert QPixmap to numpy array
    img = pixmap.toImage().convertToFormat(QImage.Format_RGB888)
    w, h = img.width(), img.height()
    ptr = img.bits()
    arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 3))

    # Define kernel for sharpening
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])

    # Apply sharpen filter using OpenCV
    sharpened_arr = cv2.filter2D(arr, -1, kernel)

    # Convert back to QPixmap
    qimg = QImage(sharpened_arr.data, w, h, 3 * w, QImage.Format_RGB888)
    pixmap_sharpened = QPixmap.fromImage(qimg)

    return pixmap_sharpened
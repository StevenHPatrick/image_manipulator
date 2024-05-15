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

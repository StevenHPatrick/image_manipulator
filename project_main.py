# signals_slots.py


"""Signals and slots example."""


import sys


from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    
)
from PySide6.QtGui import QPixmap


class Window(QMainWindow):

    def __init__(self):

        super().__init__(parent=None)
#Created a dictionary to hold on to a list of menu names and their associated functions.
        self.dict_of_menu_options = {}
        self.dict_of_toolbar_options={}

        self.setWindowTitle("QMainWindow")

        self.setCentralWidget(QLabel("I'm the Central Widget"))

        self.create_menuBar()

        self.createToolBar()

        self._createStatusBar()



    def populate_menu(self):


        menu = self.menuBar().addMenu("&Menu")
        self.create_menu_tool("&Exit", self.close)
        # This loop goes through the dictionary to populate the menu. This way, menu items can be added without having to hardcode everything
        for item, function in self.dict_of_menu_options.items():
            menu.addAction(item, function)
        
    def create_menuBar(self):
        populate_menu()

    def createToolBar(self):

        tools = QToolBar()

        #tools.addAction("Exit", self.close)
        self.create_toolbar_tool("Exit", self.close)
        for item, function in self.dict_of_menu_options.items():
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
    


if __name__ == "__main__":

    app = QApplication([])

    window = Window()

    window.show()

    sys.exit(app.exec())
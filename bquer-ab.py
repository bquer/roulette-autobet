import sys
import json
import time
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QPainter, QIcon
from PyQt5 import QtCore, QtWidgets

from click_algorithm import click_algorithm

class RouletteApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BQuer AutoBet")
        self.setGeometry(100, 100, 600, 150) 
        self.setWindowIcon(QIcon('icon.ico'))
        self.coords = self.load_coords()
        self.click_algorithm = click_algorithm
        self.create_roulette_buttons_page()

    def load_coords(self):
        with open("coords.json", "r") as f:
            return json.load(f)

    def on_button_click(self, number):
        if number in self.click_algorithm:
            algorithm = self.click_algorithm[number]
            for coord in algorithm:
                x = int(self.coords[str(coord)]["X"])
                y = int(self.coords[str(coord)]["Y"])
                pyautogui.click(x=x, y=y)
                time.sleep(0.04)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#36393F"))
        for button in self.findChildren(QPushButton):
            painter.setPen(QColor("white"))
            painter.drawRect(button.x() - 2, button.y() - 2, button.width() + 4, button.height() + 4)

    def create_roulette_buttons_page(self):
        main_layout = QVBoxLayout()

        grid_layout = QGridLayout()

        num_rows = 3
        num_columns = 12  

        black_numbers = [6, 15, 24, 33, 2, 8, 11, 17, 20, 26, 29, 35, 4, 10, 13, 22, 28, 31]

        for row in reversed(range(num_rows)):
            for col in range(num_columns):
                number = col * num_rows + row + 1
                if number > 36:  
                    continue
                button_color = "black" if number in black_numbers else "red"

                number_button = QPushButton(str(number))
                button_style = f"background-color: {button_color}; color: white; border: 2px solid white;"
                number_button.setStyleSheet(button_style)
                number_button.setFont(QFont('Helvetica', 12, QFont.Bold))
                number_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                number_button.clicked.connect(lambda _, n=number: self.on_button_click(n))

                row_span = 4 if number == 0 else 1
                col_pos = col + 2 if number == 0 else col + 1
                grid_layout.addWidget(number_button, (num_rows - 1) - row, col_pos, row_span, 1)

        zero_button = QPushButton("0", self)
        zero_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        zero_button.setStyleSheet("background-color: green; color: white; border: 2px solid white;")
        zero_button.setFont(QFont('Helvetica', 14, QFont.Bold))
        zero_button.clicked.connect(lambda: self.on_button_click(0))
        grid_layout.addWidget(zero_button, 0, 0, num_rows, 1)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

    roulette_app = RouletteApp()
    roulette_app.setWindowFlags(roulette_app.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

    roulette_app.show()
    sys.exit(app.exec_())

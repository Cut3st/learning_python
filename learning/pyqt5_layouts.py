#PyQt5 Layouts
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, 
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)
        # Call the UI setup method
        self.initUI()

    def initUI(self):
        # Create a central widget (a container for everything inside the window)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create 5 colored labels for demonstration
        label1 = QLabel("#1", self)
        label2 = QLabel("#2", self)
        label3 = QLabel("#3", self)
        label4 = QLabel("#4", self)
        label5 = QLabel("#5", self)

        # Set background color for each label
        label1.setStyleSheet("background-color: red;")
        label2.setStyleSheet("background-color: yellow;")
        label3.setStyleSheet("background-color: green;")
        label4.setStyleSheet("background-color: blue;")
        label5.setStyleSheet("background-color: purple;")

        # ========================
        # Layout Options Below 👇
        # ========================

        # VERTICAL LAYOUT (QVBoxLayout)
        # - Stacks widgets vertically (top to bottom)
        # - Use this when you want elements arranged in a column
        # vbox = QVBoxLayout()
        # vbox.addWidget(label1)
        # vbox.addWidget(label2)
        # vbox.addWidget(label3)
        # vbox.addWidget(label4)
        # vbox.addWidget(label5)
        # central_widget.setLayout(vbox)

        # HORIZONTAL LAYOUT (QHBoxLayout)
        # - Places widgets side by side (left to right)
        # - Use this when you want elements in a row
        # hbox = QHBoxLayout()
        # hbox.addWidget(label1)
        # hbox.addWidget(label2)
        # hbox.addWidget(label3)
        # hbox.addWidget(label4)
        # hbox.addWidget(label5)
        # central_widget.setLayout(hbox)

        # GRID LAYOUT (QGridLayout)
        # - Arranges widgets in a grid (rows and columns like a table)
        # - Good when you want more control over positioning
        # - Each widget is added at a specific (row, column)
        # grid = QGridLayout()
        # grid.addWidget(label1, 0, 0)  # Top-left
        # grid.addWidget(label2, 0, 1)  # Top-right
        # grid.addWidget(label3, 1, 0)  # Middle-left
        # grid.addWidget(label4, 1, 1)  # Middle-right
        # grid.addWidget(label5, 2, 2)  # Bottom-right (diagonal)
        # central_widget.setLayout(grid)

        # 💡 Only one layout should be active at a time
        # To test different ones, uncomment one layout section only


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
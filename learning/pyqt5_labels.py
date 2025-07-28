#PyQt5 Introduction
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My First GUI")
        self.setGeometry(700, 300, 500, 500)
        self.setWindowIcon(QIcon("server-icon.png"))

        label = QLabel("Hello", self)
        label.setFont(QFont("Arial", 40))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet("color: #292929;"
                            "background-color: #6fdcf7;"
                            "font-weight: bold;" 
                            "font-style: italic;"
                            "text-decoration: underline;")
        #label.setAlignment(Qt.AlignTop) VERTICALLY TOP
        #label.setAlignment(Qt.AlignBottom) VERTICALLY BOTTOM
        #label.setAlignment(Qt.AlignVCenter) VERTICVALLY CENTER
        #label.setAlignment(Qt.AlignRight) HORIZONTALLY RIGHT
        #label.setAlignment(Qt.AlignLeft) HORIZONTALLY LEFT
        label.setAlignment(Qt.AlignCenter) #HORIZONTALLY CENTER
        
        
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

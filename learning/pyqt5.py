#PyQt5 Introduction
import sys # sys is used to access command-line arguments and to exit the program cleanly
from PyQt5.QtWidgets import QApplication, QMainWindow # Import the core GUI application and main window class
from PyQt5.QtGui import QIcon # QIcon allows you to set an icon for the window

# Define a class for the main window, inheriting from QMainWindow (a basic window with a title bar, close button, etc.)
class MainWindow(QMainWindow):
    def __init__(self):
        # Call the parent constructor to initialize the QMainWindow properly
        super().__init__()

        # Set the title of the window (displayed in the title bar)
        self.setWindowTitle("My First GUI")

        # Set the size and position of the window on the screen:
        # x=700, y=300, width=500, height=500
        self.setGeometry(700, 300, 500, 500)

        # Set the icon of the window using an image file (make sure this image is in the same directory)
        self.setWindowIcon(QIcon("server-icon.png"))
        

def main():
    # Create a QApplication object, which is required for any PyQt5 app
    # It manages application-wide resources and settings
    app = QApplication(sys.argv)

    # Create an instance of the main window
    window = MainWindow()

    # Show the main window on the screen
    window.show()

    # Start the application's event loop (keeps the window open and responsive)
    # The program exits only when the window is closed
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

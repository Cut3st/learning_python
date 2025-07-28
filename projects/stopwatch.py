#Python PyQt5 Digital Clock
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget
from PyQt5.QtCore import QTimer, QTime, Qt, QDateTime
from PyQt5.QtGui import QIcon

class StopWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stop Watch")
        self.setWindowIcon(QIcon("server-icon.png"))  

        #Core Widgets
        self.start_button = QPushButton("START", self)
        self.reset_button = QPushButton("RESET", self)
        self.lap_button = QPushButton("LAP", self)
        self.lap_list = QListWidget(self)
        self.time_label = QLabel("00:00:00.00", self)

        #Time Tracking
        self.time = QTime(0,0,0,0)
        self.timer = QTimer(self)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.time_label)
        self.time_label.setAlignment(Qt.AlignCenter)


        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.reset_button)
        hbox.addWidget(self.lap_button)
        vbox.addLayout(hbox)

        vbox.addWidget(self.lap_list)

        self.start_button.clicked.connect(self.toggle_timer)
        self.reset_button.clicked.connect(self.reset)
        self.lap_button.clicked.connect(self.record_lap)
        self.timer.timeout.connect(self.update_display)

        self.start_button.setObjectName("start_button")
        self.reset_button.setObjectName("reset_button")     
        self.lap_button.setObjectName("lap_button")    
 
        self.setStyleSheet("""
            QPushButton, QLabel, QListWidget{
                padding: 20px;
                font-weight: bold;
                font-family: calibri;             
            }
            QLabel{
                font-size: 150px;
                background-color: hsl(294, 100%, 90%)      
            }
            QPushButton{
                font-size: 40px;
                font-family: Arial;
                padding: 15px 75px;
            }
            QPushButton#start_button{
                background-color: hsl(122, 100%, 64%);
            }
            QPushButton#lap_button {
                background-color: hsl(48, 100%, 64%);
            }
            QListWidget {
                font-size: 20px;
                padding: 10px;
            }
        """)

    def toggle_timer(self):
        if self.start_button.text() == "START":
            self.timer.start(10)
            self.start_button.setText("STOP")
            self.start_button.setStyleSheet("""
                background-color: hsl(0, 100%, 64%);
                font-size: 40px;
                font-family: Arial;
                padding: 15px 75px;
            """)
        else:
            self.timer.stop()
            self.start_button.setText("START")
            self.start_button.setStyleSheet("""
                background-color: hsl(122, 100%, 64%);
                font-size: 40px;
                font-family: Arial;
                padding: 15px 75px;
            """)

    def reset(self):
        self.timer.stop()
        self.time = QTime(0, 0, 0, 0)
        self.time_label.setText("00:00:00.00")
        self.start_button.setText("START")
        self.start_button.setStyleSheet("""
            background-color: hsl(122, 100%, 64%);
            font-size: 40px;
            font-family: Arial;
            padding: 15px 50px;
        """)
        self.lap_list.clear()

    def format_time(self, time):
        hr = time.hour()
        min = time.minute()
        sec = time.second()
        ms = time.msec() // 10
        return f"{hr:02}:{min:02}:{sec:02}.{ms:02}"

    def update_display(self):
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))
    
    def record_lap(self):
        if self.timer.isActive():
            lap_number = self.lap_list.count() + 1
            lap_time = self.format_time(self.time)
            current_time = QDateTime.currentDateTime().toString("HH:mm:ss AP")  # e.g. "14:23:15"
            self.lap_list.addItem(f"Lap {lap_number}: {lap_time} (at {current_time})")    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = StopWatch()
    clock.show()
    sys.exit(app.exec_())


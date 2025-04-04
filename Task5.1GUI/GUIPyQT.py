import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QRadioButton, QPushButton, QLabel, QGroupBox, 
                            QButtonGroup, QFrame, QLineEdit, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import RPi.GPIO as GPIO
import time

class LEDControllerApp(QWidget):
    
    def __init__(self):
        super().__init__()
        
        # Setting up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Defining the GPIO pins
        self.red_pin = 17    # (physical pin 11)
        self.green_pin = 27  # (physical pin 13) 
        self.blue_pin = 22   #  physical pin 15)
        
        # Setting pins as outputs
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        
        self.turn_off_all_leds()
        
        # Initializing UI
        self.initUI()
        
        # Running LED test
        self.test_led_sequence()
    
    def test_led_sequence(self):
        for pin in [self.red_pin, self.green_pin, self.blue_pin]:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.2)
        
        for _ in range(2):
            GPIO.output(self.red_pin, GPIO.HIGH)
            GPIO.output(self.green_pin, GPIO.HIGH)
            GPIO.output(self.blue_pin, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(self.red_pin, GPIO.LOW)
            GPIO.output(self.green_pin, GPIO.LOW)
            GPIO.output(self.blue_pin, GPIO.LOW)
            time.sleep(0.2)
    
    def turn_off_all_leds(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)
        
    def initUI(self):
        # Window properties
        self.setWindowTitle('LED Controller')
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title label
        title_label = QLabel('Raspberry Pi LED Controller')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Subtitle label
        subtitle_label = QLabel('Ahmad Chaudhry s224227027')
        subtitle_label.setFont(QFont('Arial', 12, QFont.Bold))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(subtitle_label)
        
        # Seperation line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(line)
        
        # Add color input section
        color_input_group = QGroupBox("Enter LED color:")
        color_input_group.setFont(QFont('Arial', 10))
        color_input_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #aaaaaa;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        color_layout = QVBoxLayout()
        
        # Instruction label
        instruction_label = QLabel("Type 'red', 'green', 'blue', or 'all' and press Enter:")
        instruction_label.setFont(QFont('Arial', 9))
        color_layout.addWidget(instruction_label)
        
        # Add color input field
        self.color_input = QLineEdit()
        self.color_input.setFont(QFont('Arial', 10))
        self.color_input.setPlaceholderText("Enter color here...")
        self.color_input.returnPressed.connect(self.color_input_entered)
        color_layout.addWidget(self.color_input)
        
        color_input_group.setLayout(color_layout)
        main_layout.addWidget(color_input_group)
        
        # Group box for radio buttons
        group_box = QGroupBox("Or select LED to illuminate:")
        group_box.setFont(QFont('Arial', 10))
        group_box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #aaaaaa;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Radio button layout
        radio_layout = QVBoxLayout()
        radio_layout.setSpacing(10)
        
        # Create button group to make radio buttons exclusive
        self.button_group = QButtonGroup(self)
        
        # Styled radio buttons
        self.red_radio = self.create_styled_radio("Red LED", "#ff6b6b")
        self.green_radio = self.create_styled_radio("Green LED", "#51cf66")
        self.blue_radio = self.create_styled_radio("Blue LED", "#339af0")
        self.all_radio = self.create_styled_radio("All LEDs", "#9f6cf7")
        
        # Adding radio buttons to button group and layout
        self.button_group.addButton(self.red_radio, 1)
        self.button_group.addButton(self.green_radio, 2)
        self.button_group.addButton(self.blue_radio, 3)
        self.button_group.addButton(self.all_radio, 4)
        
        radio_layout.addWidget(self.red_radio)
        radio_layout.addWidget(self.green_radio)
        radio_layout.addWidget(self.blue_radio)
        radio_layout.addWidget(self.all_radio)
        
        # Setting layout for group box
        group_box.setLayout(radio_layout)
        main_layout.addWidget(group_box)
        
        # Connectting radio buttons to function
        self.red_radio.toggled.connect(lambda: self.led_selected(self.red_radio))
        self.green_radio.toggled.connect(lambda: self.led_selected(self.green_radio))
        self.blue_radio.toggled.connect(lambda: self.led_selected(self.blue_radio))
        self.all_radio.toggled.connect(lambda: self.led_selected(self.all_radio))
        
        # Status label
        self.status_label = QLabel("No LED is currently active")
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #555555; margin: 10px 0;")
        main_layout.addWidget(self.status_label)
        
        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.setFont(QFont('Arial', 11, QFont.Bold))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #f03e3e;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e03131;
            }
            QPushButton:pressed {
                background-color: #c92a2a;
            }
        """)
        exit_button.clicked.connect(self.close_application)
        
        # Adding exit button to layout
        main_layout.addWidget(exit_button)
        
        # Setting main layout
        self.setLayout(main_layout)
        
    def create_styled_radio(self, text, color):
        radio = QRadioButton(text)
        radio.setFont(QFont('Arial', 11))
        radio.setStyleSheet(f"""
            QRadioButton {{
                spacing: 10px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #aaaaaa;
            }}
            QRadioButton::indicator:checked {{
                background-color: {color};
                border: 2px solid {color};
            }}
            QRadioButton::indicator:unchecked:hover {{
                border: 2px solid {color};
            }}
        """)
        return radio
    
    def color_input_entered(self):
        color = self.color_input.text().strip().lower()
        
        # Clearing any selected radio buttons
        self.button_group.setExclusive(False)
        self.red_radio.setChecked(False)
        self.green_radio.setChecked(False)
        self.blue_radio.setChecked(False)
        self.all_radio.setChecked(False)
        self.button_group.setExclusive(True)
        
        self.turn_off_all_leds()
        
        # Processing color input
        if color == "red":
            GPIO.output(self.red_pin, GPIO.HIGH)
            self.status_label.setText("Red LED is ON")
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        elif color == "green":
            GPIO.output(self.green_pin, GPIO.HIGH)
            self.status_label.setText("Green LED is ON")
            self.status_label.setStyleSheet("color: #51cf66; font-weight: bold;")
        elif color == "blue":
            GPIO.output(self.blue_pin, GPIO.HIGH)
            self.status_label.setText("Blue LED is ON")
            self.status_label.setStyleSheet("color: #339af0; font-weight: bold;")
        elif color == "all":
            GPIO.output(self.red_pin, GPIO.HIGH)
            GPIO.output(self.green_pin, GPIO.HIGH)
            GPIO.output(self.blue_pin, GPIO.HIGH)
            self.status_label.setText("All LEDs are ON")
            self.status_label.setStyleSheet("color: #9f6cf7; font-weight: bold;")
        else:
            self.status_label.setText(f"Unknown color: {color}")
            self.status_label.setStyleSheet("color: #555555;")
        
        self.color_input.clear()
        
    def led_selected(self, radio):
        if radio.isChecked():
            self.turn_off_all_leds()
            
            if radio == self.red_radio:
                GPIO.output(self.red_pin, GPIO.HIGH)
                self.status_label.setText("Red LED is ON")
                self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            elif radio == self.green_radio:
                GPIO.output(self.green_pin, GPIO.HIGH) 
                self.status_label.setText("Green LED is ON")
                self.status_label.setStyleSheet("color: #51cf66; font-weight: bold;")
            elif radio == self.blue_radio:
                GPIO.output(self.blue_pin, GPIO.HIGH)
                self.status_label.setText("Blue LED is ON")
                self.status_label.setStyleSheet("color: #339af0; font-weight: bold;")
            elif radio == self.all_radio:
                GPIO.output(self.red_pin, GPIO.HIGH)
                GPIO.output(self.green_pin, GPIO.HIGH)
                GPIO.output(self.blue_pin, GPIO.HIGH)
                self.status_label.setText("All LEDs are ON")
                self.status_label.setStyleSheet("color: #9f6cf7; font-weight: bold;")
    
    def close_application(self):
        self.turn_off_all_leds()
        GPIO.cleanup()
        QApplication.quit()
        
    def closeEvent(self, event):
        GPIO.cleanup()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LEDControllerApp()
    window.show()
    sys.exit(app.exec_())
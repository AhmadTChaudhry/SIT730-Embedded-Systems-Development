import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QSlider, QPushButton, QLabel, QGroupBox, 
                            QFrame, QHBoxLayout, QInputDialog, QSpinBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import RPi.GPIO as GPIO
import time

class PWMLEDControllerApp(QWidget):
    
    def __init__(self):
        super().__init__()
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.red_pin = 17    # (physical pin 11)
        self.green_pin = 27  # (physical pin 13) 
        self.blue_pin = 22   # (physical pin 15)
        
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        
        # Initialize PWM on each pin (frequency = 100Hz)
        self.red_pwm = GPIO.PWM(self.red_pin, 100)
        self.green_pwm = GPIO.PWM(self.green_pin, 100)
        self.blue_pwm = GPIO.PWM(self.blue_pin, 100)
        
        # Start PWM with 0% duty cycle
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
        
        self.red_value = 0
        self.green_value = 0
        self.blue_value = 0
        
        self.initUI()
        
        self.test_led_sequence()
    
    def test_led_sequence(self):
        for pwm_obj in [self.red_pwm, self.green_pwm, self.blue_pwm]:
            for duty in [30, 60, 100]:
                pwm_obj.ChangeDutyCycle(duty)
                time.sleep(0.2)
            pwm_obj.ChangeDutyCycle(0)
            time.sleep(0.2)
        
        for duty in [30, 60, 100, 0]:
            self.red_pwm.ChangeDutyCycle(duty)
            self.green_pwm.ChangeDutyCycle(duty)
            self.blue_pwm.ChangeDutyCycle(duty)
            time.sleep(0.3)
    
    def turn_off_all_leds(self):
        self.red_pwm.ChangeDutyCycle(0)
        self.green_pwm.ChangeDutyCycle(0)
        self.blue_pwm.ChangeDutyCycle(0)
        self.red_value = 0
        self.green_value = 0
        self.blue_value = 0
        
    def initUI(self):
        self.setWindowTitle('PWM LED Controller')
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        title_label = QLabel('Raspberry Pi PWM LED Controller')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        subtitle_label = QLabel('Ahmad Chaudhry s224227027')
        subtitle_label.setFont(QFont('Arial', 12, QFont.Bold))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(subtitle_label)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(line)
        
        # Creating sliders group box
        sliders_group = QGroupBox("LED Intensity Control")
        sliders_group.setFont(QFont('Arial', 10))
        sliders_group.setStyleSheet("""
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
        
        # Sliders layout
        sliders_layout = QVBoxLayout()
        sliders_layout.setSpacing(15)
        
        # Red LED slider
        red_layout = QHBoxLayout()
        red_label = QLabel("Red LED:")
        red_label.setFont(QFont('Arial', 11))
        red_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        red_layout.addWidget(red_label, 1)
        
        self.red_slider = QSlider(Qt.Horizontal)
        self.setup_slider(self.red_slider)
        self.red_slider.valueChanged.connect(self.red_slider_changed)
        red_layout.addWidget(self.red_slider, 4)
        
        self.red_value_label = QLabel("0%")
        self.red_value_label.setFont(QFont('Arial', 11))
        self.red_value_label.setMinimumWidth(40)
        self.red_value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        red_layout.addWidget(self.red_value_label, 1)
        
        sliders_layout.addLayout(red_layout)
        
        # Green LED slider
        green_layout = QHBoxLayout()
        green_label = QLabel("Green LED:")
        green_label.setFont(QFont('Arial', 11))
        green_label.setStyleSheet("color: #51cf66; font-weight: bold;")
        green_layout.addWidget(green_label, 1)
        
        self.green_slider = QSlider(Qt.Horizontal)
        self.setup_slider(self.green_slider)
        self.green_slider.valueChanged.connect(self.green_slider_changed)
        green_layout.addWidget(self.green_slider, 4)
        
        self.green_value_label = QLabel("0%")
        self.green_value_label.setFont(QFont('Arial', 11))
        self.green_value_label.setMinimumWidth(40)
        self.green_value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        green_layout.addWidget(self.green_value_label, 1)
        
        sliders_layout.addLayout(green_layout)
        
        # Blue LED slider
        blue_layout = QHBoxLayout()
        blue_label = QLabel("Blue LED:")
        blue_label.setFont(QFont('Arial', 11))
        blue_label.setStyleSheet("color: #339af0; font-weight: bold;")
        blue_layout.addWidget(blue_label, 1)
        
        self.blue_slider = QSlider(Qt.Horizontal)
        self.setup_slider(self.blue_slider)
        self.blue_slider.valueChanged.connect(self.blue_slider_changed)
        blue_layout.addWidget(self.blue_slider, 4)
        
        self.blue_value_label = QLabel("0%")
        self.blue_value_label.setFont(QFont('Arial', 11))
        self.blue_value_label.setMinimumWidth(40)
        self.blue_value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        blue_layout.addWidget(self.blue_value_label, 1)
        
        sliders_layout.addLayout(blue_layout)
        
        # Preview box for color
        self.color_preview = QFrame()
        self.color_preview.setFrameShape(QFrame.Box)
        self.color_preview.setFrameShadow(QFrame.Sunken)
        self.color_preview.setLineWidth(2)
        self.color_preview.setMinimumHeight(50)
        self.color_preview.setStyleSheet("background-color: #000000; border-radius: 5px;")
        sliders_layout.addWidget(self.color_preview)
        
        sliders_group.setLayout(sliders_layout)
        main_layout.addWidget(sliders_group)
        
        # Control buttons
        buttons_layout = QHBoxLayout()
        
        # Full brightness button
        all_max_button = QPushButton("Full Brightness")
        all_max_button.setFont(QFont('Arial', 10, QFont.Bold))
        all_max_button.setStyleSheet("""
            QPushButton {
                background-color: #4dabf7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #3b8fd7;
            }
            QPushButton:pressed {
                background-color: #2b7fc7;
            }
        """)
        all_max_button.clicked.connect(self.all_leds_max)
        buttons_layout.addWidget(all_max_button)
        
        # Fade button
        fade_button = QPushButton("Fade Effect")
        fade_button.setFont(QFont('Arial', 10, QFont.Bold))
        fade_button.setStyleSheet("""
            QPushButton {
                background-color: #ae3ec9;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #9c36b5;
            }
            QPushButton:pressed {
                background-color: #862e9c;
            }
        """)
        fade_button.clicked.connect(self.show_fade_dialog)
        buttons_layout.addWidget(fade_button)
        
        # Turn off button
        turn_off_button = QPushButton("Turn Off All")
        turn_off_button.setFont(QFont('Arial', 10, QFont.Bold))
        turn_off_button.setStyleSheet("""
            QPushButton {
                background-color: #868e96;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #666e76;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        turn_off_button.clicked.connect(self.reset_leds)
        buttons_layout.addWidget(turn_off_button)
        
        main_layout.addLayout(buttons_layout)
        
        self.status_label = QLabel("Adjust sliders to control LED brightness")
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
    
    def setup_slider(self, slider):
        slider.setRange(0, 100)
        slider.setValue(0)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 10px;
                background: #dddddd;
                border-radius: 5px;
            }
            
            QSlider::handle:horizontal {
                background: #5c7cfa;
                border: 2px solid #5c7cfa;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -8px 0;
            }
            
            QSlider::handle:horizontal:hover {
                background: #4c6ef5;
                border: 2px solid #4c6ef5;
            }
            
            QSlider::sub-page:horizontal {
                background: #adb5bd;
                border-radius: 5px;
            }
        """)
    
    def update_color_preview(self):
        # Converting PWM values to hex format for RGB
        r_hex = int(self.red_value * 2.55)
        g_hex = int(self.green_value * 2.55)
        b_hex = int(self.blue_value * 2.55)
        
        # CSS RGB color string
        color = f"rgb({r_hex}, {g_hex}, {b_hex})"
        
        # Updating preview color
        self.color_preview.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
    
    def red_slider_changed(self, value):
        self.red_value = value
        self.red_value_label.setText(f"{value}%")
        self.red_pwm.ChangeDutyCycle(value)
        self.update_status()
        self.update_color_preview()
    
    def green_slider_changed(self, value):
        self.green_value = value
        self.green_value_label.setText(f"{value}%")
        self.green_pwm.ChangeDutyCycle(value)
        self.update_status()
        self.update_color_preview()
    
    def blue_slider_changed(self, value):
        self.blue_value = value
        self.blue_value_label.setText(f"{value}%")
        self.blue_pwm.ChangeDutyCycle(value)
        self.update_status()
        self.update_color_preview()
    
    def update_status(self):
        if self.red_value == 0 and self.green_value == 0 and self.blue_value == 0:
            self.status_label.setText("All LEDs are OFF")
            self.status_label.setStyleSheet("color: #555555;")
        else:
            active_leds = []
            if self.red_value > 0:
                active_leds.append(f"Red ({self.red_value}%)")
            if self.green_value > 0:
                active_leds.append(f"Green ({self.green_value}%)")
            if self.blue_value > 0:
                active_leds.append(f"Blue ({self.blue_value}%)")
            
            led_text = " + ".join(active_leds)
            self.status_label.setText(f"Active LEDs: {led_text}")
            
            # Setting color based on which LED is brightest
            if self.red_value >= self.green_value and self.red_value >= self.blue_value:
                self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            elif self.green_value >= self.red_value and self.green_value >= self.blue_value:
                self.status_label.setStyleSheet("color: #51cf66; font-weight: bold;")
            else:
                self.status_label.setStyleSheet("color: #339af0; font-weight: bold;")
    
    def all_leds_max(self):
        self.red_slider.setValue(100)
        self.green_slider.setValue(100)
        self.blue_slider.setValue(100)
    
    def reset_leds(self):
        self.red_slider.setValue(0)
        self.green_slider.setValue(0)
        self.blue_slider.setValue(0)
        self.status_label.setText("All LEDs are OFF")
        self.status_label.setStyleSheet("color: #555555;")
    
    def fade_leds(self, duration_seconds):
        self.status_label.setText(f"Fading LEDs for {duration_seconds} seconds...")
        self.status_label.setStyleSheet("color: #5c7cfa; font-weight: bold;")
        
        # Original values
        original_red = self.red_value
        original_green = self.green_value
        original_blue = self.blue_value
        
        steps = 100  # Number of steps for the fade
        delay = duration_seconds / (steps * 2)  # Total time divided by fade-in + fade-out
        
        # Disable sliders during animation
        self.red_slider.setEnabled(False)
        self.green_slider.setEnabled(False)
        self.blue_slider.setEnabled(False)
        
        try:
            # Fade in
            for i in range(0, 101, 1):
                self.red_pwm.ChangeDutyCycle(i)
                self.green_pwm.ChangeDutyCycle(i)
                self.blue_pwm.ChangeDutyCycle(i)
                # Update UI
                self.red_value = i
                self.green_value = i
                self.blue_value = i
                self.red_value_label.setText(f"{i}%")
                self.green_value_label.setText(f"{i}%")
                self.blue_value_label.setText(f"{i}%")
                self.update_color_preview()
                QApplication.processEvents()  
                time.sleep(delay)
                
            # Fade out
            for i in range(100, -1, -1):
                self.red_pwm.ChangeDutyCycle(i)
                self.green_pwm.ChangeDutyCycle(i)
                self.blue_pwm.ChangeDutyCycle(i)
                # Update UI
                self.red_value = i
                self.green_value = i
                self.blue_value = i
                self.red_value_label.setText(f"{i}%")
                self.green_value_label.setText(f"{i}%")
                self.blue_value_label.setText(f"{i}%")
                self.update_color_preview()
                QApplication.processEvents()  
                time.sleep(delay)
                
            # Restore original values
            self.red_slider.setValue(original_red)
            self.green_slider.setValue(original_green)
            self.blue_slider.setValue(original_blue)
            
            self.status_label.setText("Fade complete!")
        finally:
            # Re-enable sliders even if interrupted
            self.red_slider.setEnabled(True)
            self.green_slider.setEnabled(True)
            self.blue_slider.setEnabled(True)
    
    def show_fade_dialog(self):
        duration, ok = QInputDialog.getInt(
            self, 
            "Fade Duration", 
            "Enter fade duration in seconds (1-30):",
            value=5,
            min=1,
            max=30,
            step=1
        )
        
        if ok:
            self.fade_leds(duration)
    
    def close_application(self):
        self.turn_off_all_leds()
        GPIO.cleanup()
        QApplication.quit()
        
    def closeEvent(self, event):
        self.turn_off_all_leds()
        GPIO.cleanup()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PWMLEDControllerApp()
    window.show()
    sys.exit(app.exec_())
#!/usr/bin/env python3
import threading
import tkinter as tk
from tkinter import StringVar
import speech_recognition as sr
from lifxlan import Light

# Bulb details
bulb = {"ip": "192.168.0.200", "mac": "D0:73:D5:24:81:05"}
light = Light(bulb["mac"], bulb["ip"])

# Initializing recognizer
recognizer = sr.Recognizer()

# GUI setup
def create_gui():
    window = tk.Tk()
    window.title("Voice Light Control")
    window.geometry("300x200")

    status_var = StringVar()
    status_var.set("Ready")

    def update_status(new_status):
        status_var.set(new_status)
        if new_status == "ON":
            status_label.config(fg="green")
        elif new_status == "OFF":
            status_label.config(fg="red")
        else:
            status_label.config(fg="black")

    def process_command(command):
        command = command.lower()
        print(f"You said: {command}")

        if "on" in command:
            light.set_power("on")
            update_status("ON")
            print(f"Turned ON bulb {bulb['mac']} at {bulb['ip']}")
        elif "off" in command:
            light.set_power("off")
            update_status("OFF")
            print(f"Turned OFF bulb {bulb['mac']} at {bulb['ip']}")
        else:
            print("Didn't recognize a valid command. Please say 'on' or 'off'.")

    def listen_loop():
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Ready. Say 'on' or 'off' anytime...")

            while True:
                try:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    process_command(command)
                except sr.WaitTimeoutError:
                    print("Timeout — no speech detected. Listening again...")
                except sr.UnknownValueError:
                    print("Could not understand audio. Try again.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                except KeyboardInterrupt:
                    print("\nExiting. Goodbye!")
                    break

    def start_listening():
        threading.Thread(target=listen_loop, daemon=True).start()

    tk.Label(window, text="Ahmad Chaudhry - s224227027", font=("Helvetica", 10)).pack(pady=5)
    tk.Label(window, text="Light Status:", font=("Helvetica", 16)).pack(pady=10)

    status_label = tk.Label(window, textvariable=status_var, font=("Helvetica", 24, "bold"), fg="black")
    status_label.pack()

    tk.Button(window, text="Start Listening", command=start_listening, font=("Helvetica", 12)).pack(pady=5)

    tk.Button(window, text="Exit", command=window.destroy, font=("Helvetica", 12), fg="red").pack(pady=5)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
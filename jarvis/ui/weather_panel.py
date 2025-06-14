import hashlib
import os

import customtkinter as ctk
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from jarvis.modules.weather import get_weather

class WeatherPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.city_var = ctk.StringVar(value="Warsaw")

        self.label = ctk.CTkLabel(self, text="City:")
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.city_entry = ctk.CTkEntry(self, textvariable=self.city_var)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        self.button = ctk.CTkButton(self, text="Refresh", command=self.refresh_weather)
        self.button.grid(row=0, column=2, padx=5, pady=5)

        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.grid(row=1, column=0, columnspan=3)

        self.weather_label = ctk.CTkLabel(self, font=("Arial", 16))
        self.weather_label.grid(row=2, column=0, columnspan=3)

        self.weather_icon = None
        self.refresh_weather()

    def refresh_weather(self):
        city = self.city_var.get()
        weather, error = get_weather(city)
        if error:
            messagebox.showerror("Error", error)
            return
        temp_c, condition, icon_url = weather

        icon_hash = hashlib.md5(icon_url.encode('utf-8')).hexdigest()
        icon_filename = f"{icon_hash}.png"

        icon_dir = os.path.join("resources", "icons")
        os.makedirs(icon_dir, exist_ok=True)
        icon_path = os.path.join(icon_dir, icon_filename)

        try:
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
            else:
                response = requests.get(icon_url)
                response.raise_for_status()
                with open(icon_path, 'wb') as f:
                    f.write(response.content)
                image = Image.open(icon_path)

            self.weather_icon = ctk.CTkImage(light_image=image, size=(80, 80))
            self.icon_label.configure(image=self.weather_icon, text="")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.icon_label.configure(text="❓", image=None)

        self.weather_label.configure(text=f"{city}: {temp_c}°C, {condition}")
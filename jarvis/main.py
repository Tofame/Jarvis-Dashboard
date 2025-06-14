import customtkinter as ctk

from jarvis.ui.crypto_panel import CryptoPanel
from jarvis.ui.weather_panel import WeatherPanel
from jarvis.ui.stocks_panel import StocksPanel
from jarvis.ui.currencies_panel import CurrenciesPanel
from dotenv import load_dotenv

class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS Dashboard")
        self.geometry("1200x700")

        for i in range(3):
            self.grid_columnconfigure(i, weight=1, uniform="panel")
        self.grid_rowconfigure(0, weight=1)

        # ----------- Left panel (weather + currencies)
        left_panel = ctk.CTkFrame(self)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)

        # Weather panel container
        weather_container = ctk.CTkFrame(left_panel)
        weather_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        weather_container.grid_columnconfigure(0, weight=1)
        weather_container.grid_rowconfigure(0, weight=1)
        #weather_panel = WeatherPanel(weather_container)
        #weather_panel.pack(expand=True, anchor="center")

        # Currencies panel container
        currencies_container = ctk.CTkFrame(left_panel)
        currencies_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        currencies_container.grid_columnconfigure(0, weight=1)
        currencies_container.grid_rowconfigure(0, weight=1)
        #currencies_panel = CurrenciesPanel(currencies_container)
        #currencies_panel.pack(anchor="n", pady=10)

        # ----------- Center panel (notes) container
        center_panel = ctk.CTkFrame(self)
        center_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        center_panel.grid_columnconfigure(0, weight=1)
        center_panel.grid_rowconfigure(0, weight=1)

        # TO-DO Notes Panel
        # notes_container = ctk.CTkFrame(center_panel)
        # notes_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        # notes_container.grid_columnconfigure(0, weight=1)
        # notes_container.grid_rowconfigure(0, weight=1)
        # notes_panel = NotesPanel(notes_container)
        # notes_panel.pack(expand=True, anchor="center")

        # ----------- Right panel (stocks + crypto)
        right_panel = ctk.CTkFrame(self)
        right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)

        # Stocks panel container
        stocks_container = ctk.CTkFrame(right_panel)
        stocks_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        stocks_container.grid_columnconfigure(0, weight=1)
        stocks_container.grid_rowconfigure(0, weight=1)
        #stocks_panel = StocksPanel(stocks_container)
        #stocks_panel.pack(expand=True, anchor="center")

        # Crypto panel container example (if you add it later)
        crypto_container = ctk.CTkFrame(right_panel)
        crypto_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        crypto_container.grid_columnconfigure(0, weight=1)
        crypto_container.grid_rowconfigure(0, weight=1)
        #crypto_panel = CryptoPanel(crypto_container)
        #crypto_panel.pack(expand=True, anchor="center")


if __name__ == "__main__":
    load_dotenv()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = JarvisApp()
    app.mainloop()

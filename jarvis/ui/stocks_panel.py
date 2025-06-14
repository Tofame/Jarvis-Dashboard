import customtkinter as ctk
from jarvis.modules.stocks import get_stock_price, get_watched_stocks, save_watched_stocks

class StocksPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.watched_stocks = get_watched_stocks()

        self.title_label = ctk.CTkLabel(self, text="Stock Market", font=ctk.CTkFont(size=18))
        self.title_label.pack(pady=(10, 5))

        self.stock_frame = ctk.CTkScrollableFrame(self, height=300)
        self.stock_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Container for stock row widgets (frame, label, button)
        self.stock_rows = {}

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=10, pady=10)

        self.new_stock_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(controls, placeholder_text="Add stock symbol (e.g. AAPL)", textvariable=self.new_stock_var)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.add_button = ctk.CTkButton(controls, text="Add", command=self.add_stock)
        self.add_button.pack(side="left", padx=(0, 5))

        self.refresh_button = ctk.CTkButton(controls, text="Force Refresh", command=self.force_refresh)
        self.refresh_button.pack(side="left")

        self.update_stocks()

    def update_stocks(self, force_refresh=False):
        # Clear old widgets
        for row in self.stock_rows.values():
            row.destroy()
        self.stock_rows.clear()

        for symbol in self.watched_stocks:
            price = get_stock_price(symbol, force_refresh=force_refresh)
            text = f"{symbol}: {price} USD" if price != "Brak danych" else f"{symbol}: No data"

            # Create a frame for each stock (label + remove button)
            row_frame = ctk.CTkFrame(self.stock_frame)
            row_frame.pack(fill="x", pady=2)

            label = ctk.CTkLabel(row_frame, text=text, font=ctk.CTkFont(size=14))
            label.pack(side="left", padx=(5, 10))

            remove_btn = ctk.CTkButton(row_frame, text="Remove", width=80,
                                       command=lambda s=symbol: self.remove_stock(s))
            remove_btn.pack(side="right", padx=5)

            self.stock_rows[symbol] = row_frame

    def add_stock(self):
        symbol = self.new_stock_var.get().strip().upper()
        if symbol == "":
            return

        if symbol in self.watched_stocks:
            return

        self.watched_stocks.append(symbol)
        save_watched_stocks(self.watched_stocks)
        self.new_stock_var.set("")
        self.update_stocks()

    def remove_stock(self, symbol):
        if symbol in self.watched_stocks:
            self.watched_stocks.remove(symbol)
            save_watched_stocks(self.watched_stocks)
            self.update_stocks()

    def force_refresh(self):
        self.update_stocks(force_refresh=True)
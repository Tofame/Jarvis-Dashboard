import hashlib
import os

import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from jarvis.modules.crypto import get_crypto_data, get_watched_cryptos, save_watched_cryptos

class CryptoPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.watched_coins = get_watched_cryptos()

        self.title_label = ctk.CTkLabel(self, text="Cryptocurrency Prices", font=ctk.CTkFont(size=18))
        self.title_label.pack(pady=(10, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, height=300)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.coin_widgets = {}

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", padx=10, pady=10)

        self.new_coin_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(controls, placeholder_text="Add coin ID (e.g. bitcoin)", textvariable=self.new_coin_var)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.add_button = ctk.CTkButton(controls, text="Add", command=self.add_coin)
        self.add_button.pack(side="left", padx=(0, 5))

        self.refresh_button = ctk.CTkButton(controls, text="Force Refresh", command=self.force_refresh)
        self.refresh_button.pack(side="left")

        self.update_coins()

    def update_coins(self, force_refresh=False):
        # Clear old widgets
        for widgets in self.coin_widgets.values():
            for w in widgets:
                w.destroy()
        self.coin_widgets.clear()

        data = get_crypto_data(self.watched_coins, force_refresh=force_refresh)

        icon_dir = os.path.join("resources", "icons")
        os.makedirs(icon_dir, exist_ok=True)

        for coin_id in self.watched_coins:
            info = data.get(coin_id)
            if not info:
                continue

            frame = ctk.CTkFrame(self.scroll_frame)
            frame.pack(fill="x", pady=5)

            icon_url = info.get("icon", "")
            icon_hash = hashlib.md5(icon_url.encode("utf-8")).hexdigest()
            icon_filename = f"{icon_hash}.png"
            icon_path = os.path.join(icon_dir, icon_filename)

            # Load icon from disk or download it
            try:
                if os.path.exists(icon_path):
                    image = Image.open(icon_path).resize((32, 32))
                else:
                    response = requests.get(icon_url)
                    response.raise_for_status()
                    with open(icon_path, "wb") as f:
                        f.write(response.content)
                    image = Image.open(icon_path).resize((32, 32))

                icon = ctk.CTkImage(light_image=image, size=(32, 32))
            except Exception as e:
                print(f"Error loading icon for {coin_id}: {e}")
                icon = None

            icon_label = ctk.CTkLabel(frame, image=icon, text="")
            icon_label.pack(side="left", padx=5)
            icon_label.image = icon  # keep reference!

            # Show name, symbol, price
            text_label = ctk.CTkLabel(
                frame,
                text=f"{info['name']} ({info['symbol']}): ${info['price']:.2f}",
                font=ctk.CTkFont(size=14)
            )
            text_label.pack(side="left", padx=5)

            # Remove button
            remove_btn = ctk.CTkButton(frame, text="Remove", width=60, command=lambda cid=coin_id: self.remove_coin(cid))
            remove_btn.pack(side="right", padx=5)

            self.coin_widgets[coin_id] = (frame, icon_label, text_label, remove_btn)

    def add_coin(self):
        new_coin = self.new_coin_var.get().strip().lower()
        if new_coin == "":
            return
        if new_coin in self.watched_coins:
            return
        self.watched_coins.append(new_coin)
        save_watched_cryptos(self.watched_coins)  # save updated list
        self.new_coin_var.set("")
        self.update_coins(force_refresh=True)

    def remove_coin(self, coin_id):
        if coin_id in self.watched_coins:
            self.watched_coins.remove(coin_id)
            save_watched_cryptos(self.watched_coins)  # save updated list
            self.update_coins(force_refresh=True)

    def force_refresh(self):
        self.update_coins(force_refresh=True)
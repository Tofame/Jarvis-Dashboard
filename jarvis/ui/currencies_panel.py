import customtkinter as ctk
from tkinter import messagebox
from jarvis.modules.currencies import get_rates, get_available_currencies
from jarvis.ui.drag_drop_list import DragDropList  # your drag & drop class

class CurrenciesPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_var = ctk.StringVar(value="PLN")
        self.followed_currencies = ["USD", "EUR", "GBP"]

        self.available_currencies, error = get_available_currencies()
        if error:
            messagebox.showwarning("Warning", f"Could not fetch available currencies: {error}")

        # Dropdown menu for base currency, with PLN at the top.
        base_values = ["PLN"] + sorted([c for c in self.available_currencies.keys() if c != "PLN"])

        self.base_label = ctk.CTkLabel(self, text="Base Currency:")
        self.base_label.grid(row=0, column=0, padx=5, pady=5)
        self.base_combo = ctk.CTkComboBox(
            self,
            values=base_values,
            variable=self.base_var,
            width=80,
        )
        self.base_combo.grid(row=0, column=1, padx=5, pady=5)

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh_rates)
        self.refresh_button.grid(row=0, column=2, padx=5, pady=5)

        # Add currency dropdown and button
        self.new_currency_var = ctk.StringVar()
        self.add_currency_combo = ctk.CTkComboBox(
            self,
            values=sorted(self.available_currencies.keys()),
            variable=self.new_currency_var,
            width=80,
        )
        self.add_currency_combo.grid(row=0, column=3, padx=5, pady=5)
        self.add_button = ctk.CTkButton(self, text="Add Currency", command=self.add_currency)
        self.add_button.grid(row=0, column=4, padx=5, pady=5)

        # Make row 1 expandable vertically for the list
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(tuple(range(5)), weight=1)

        # Scrollable frame for DragDropList
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=300, height=200)
        self.scrollable_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

        # DragDropList
        self.dd_list = DragDropList(
            self.scrollable_frame,
            items=[],
            on_reorder=self.on_reorder,
            on_remove=self.on_remove_currency
        )
        self.dd_list.pack(fill="both", expand=True)

        self.refresh_rates()

    def refresh_rates(self):
        base = self.base_var.get().upper()
        symbols = self.followed_currencies
        rates, error = get_rates(base, symbols)
        if error:
            messagebox.showwarning("Warning", error)

        # Update DragDropList items with formatted rate labels
        items_with_rates = []
        for curr in symbols:
            rate = rates.get(curr, "N/A")
            items_with_rates.append(f"1 {base} = {rate} {curr}")

        self.dd_list.items = items_with_rates
        self.dd_list.render()

    def add_currency(self):
        new_curr = self.new_currency_var.get().upper()
        if not new_curr:
            messagebox.showinfo("Info", "Please select a currency from the list.")
            return

        if new_curr in self.followed_currencies:
            messagebox.showinfo("Info", f"Currency {new_curr} is already added.")
            return

        rates, error = get_rates(base=self.base_var.get().upper(), symbols=[new_curr])
        if error:
            messagebox.showerror("Error", f"Cannot add currency: {error}")
            return

        self.followed_currencies.append(new_curr)
        self.new_currency_var.set("")
        self.refresh_rates()

    def on_reorder(self, new_items):
        new_order = [item.split()[-1] for item in new_items]
        self.followed_currencies = new_order
        self.refresh_rates()

    def on_remove_currency(self, item):
        curr = item.split()[-1]
        if curr in self.followed_currencies:
            self.followed_currencies.remove(curr)
            self.refresh_rates()
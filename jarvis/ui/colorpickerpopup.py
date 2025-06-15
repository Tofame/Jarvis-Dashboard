import customtkinter as ctk

class ColorPickerPopup(ctk.CTkToplevel):
    def __init__(self, master, callback, x=0, y=0):
        super().__init__(master)
        self.callback = callback
        self.title("Pick a Color")
        self.geometry("280x60")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # Position popup at (x, y)
        self.geometry(f"+{x}+{y}")

        self.colors = [
            "#fef3c7", "#e0f2fe", "#fce7f3",
            "#e7f6d5", "#ffadad", "#ffd6a5",
            "#caffbf", "#9bf6ff", "#a0c4ff"
        ]

        for i, color in enumerate(self.colors):
            btn = ctk.CTkButton(self, text="", width=25, height=25, fg_color=color,
                                hover_color=color, command=lambda c=color: self.select_color(c))
            btn.grid(row=0, column=i, padx=3, pady=10)

    def select_color(self, color):
        self.callback(color)
        self.destroy()
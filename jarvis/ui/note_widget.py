import customtkinter as ctk
import tkinter as tk
from jarvis.ui.colorpickerpopup import ColorPickerPopup

class Note(ctk.CTkFrame):
    def __init__(self, master, remove_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.remove_callback = remove_callback

        self.is_persistent = tk.BooleanVar(value=True)

        # Text area for the note
        self.text_widget = tk.Text(self, height=5, wrap="word", bg="#fef3c7", font=("Segoe UI", 12))
        self.text_widget.tag_configure("bold", font=("Segoe UI", 12, "bold"))
        self.text_widget.pack(padx=5, pady=5, fill="both", expand=True)

        # Buttons row
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=5, pady=5)

        self.persistent_toggle = ctk.CTkCheckBox(button_frame, text="Persistent", variable=self.is_persistent)
        self.persistent_toggle.pack(side="left", padx=2)

        self.color_button = ctk.CTkButton(button_frame, text="🎨", width=30, command=self.pick_color)
        self.color_button.pack(side="left", padx=2)

        self.bold_button = ctk.CTkButton(button_frame, text="B", width=30, command=self.make_bold)
        self.bold_button.pack(side="left", padx=2)

        self.delete_button = ctk.CTkButton(button_frame, text="❌", width=30, command=self.delete_note)
        self.delete_button.pack(side="right", padx=2)

    def pick_color(self):
        # Get absolute position of color_button on screen
        x = self.color_button.winfo_rootx()
        y = self.color_button.winfo_rooty() - 70 # Showing popup a bit above
        ColorPickerPopup(self, lambda c: self.text_widget.config(bg=c), x, y)

    def make_bold(self):
        try:
            start = self.text_widget.index(tk.SEL_FIRST)
            end = self.text_widget.index(tk.SEL_LAST)
            # Check if "bold" tag already applied in selection
            current_tags = self.text_widget.tag_names(start)
            if "bold" in current_tags:
                self.text_widget.tag_remove("bold", start, end)
            else:
                self.text_widget.tag_add("bold", start, end)
        except tk.TclError:
            pass

    def delete_note(self):
        self.remove_callback(self)

    def get_content(self):
        return self.text_widget.get("1.0", "end-1c")

    def set_content(self, content):
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", content)

    def is_note_persistent(self):
        return self.is_persistent.get()

    def get_formatting(self):
        # Collect all bold tag ranges as (start, end)
        ranges = []
        start_index = "1.0"
        while True:
            next_range = self.text_widget.tag_nextrange("bold", start_index)
            if not next_range:
                break
            start, end = next_range
            ranges.append((start, end))
            start_index = end
        # Get bg color of the text widget
        bg = self.text_widget.cget("bg")

        return {
            "bold_ranges": ranges,
            "bg_color": bg
        }

    def apply_formatting(self, formatting):
        if not formatting:
            return
        # Apply background color
        if "bg_color" in formatting:
            self.text_widget.config(bg=formatting["bg_color"])

        # Apply bold ranges
        if "bold_ranges" in formatting:
            for start, end in formatting["bold_ranges"]:
                self.text_widget.tag_add("bold", start, end)
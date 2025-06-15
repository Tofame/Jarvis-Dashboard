import logging
import tkinter as tk
import customtkinter as ctk
from jarvis.ui.note_widget import Note

class NotesPanel(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.notes = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.add_button = ctk.CTkButton(self, text="➕ Add Note", command=self.add_note)
        self.add_button.grid(row=0, column=0, sticky="ew", pady=(5, 2), padx=5)

        self.canvas = tk.Canvas(self, bg="#2c2c3e", highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.save_button = ctk.CTkButton(self, text="💾 Save Notes", command=self.save_notes)
        self.save_button.grid(row=2, column=0, sticky="ew", pady=(2, 5), padx=5)

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        # Bind mouse wheel scroll events
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        scrollbar_width = self.scrollbar.winfo_width() or 15
        new_width = canvas_width - scrollbar_width - 5

        # Resize the canvas window containing scrollable_frame
        self.canvas.itemconfig(self.canvas_window, width=new_width)
        self.scrollable_frame.configure(width=new_width)

        # Resize notes width
        for note in self.notes:
            note.configure(width=new_width - 10)

    def add_note(self):
        note = Note(self.scrollable_frame, remove_callback=self.remove_note)
        note.pack(padx=5, pady=5)
        self.notes.append(note)

        self._on_canvas_configure(None)

    def _on_canvas_configure(self, event):
        if event is not None:
            canvas_width = event.width
        else:
            canvas_width = self.canvas.winfo_width()

        scrollbar_width = self.scrollbar.winfo_width() or 15
        new_width = canvas_width - scrollbar_width + 10

        # Resize the canvas window containing scrollable_frame
        self.canvas.itemconfig(self.canvas_window, width=new_width)
        self.scrollable_frame.configure(width=new_width)

        # Resize notes width
        for note in self.notes:
            note.configure(width=new_width - 10)

    def remove_note(self, note):
        note.destroy()
        self.notes.remove(note)

    def save_notes(self):
        persistent_notes = [note.get_content() for note in self.notes if note.is_note_persistent()]
        logging.info(f"Saving persistent notes: {persistent_notes}")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
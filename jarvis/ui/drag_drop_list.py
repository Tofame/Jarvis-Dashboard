import customtkinter as ctk

# Helper class for making DragDropList, was only edited by me.
class DragDropList(ctk.CTkFrame):
    def __init__(self, parent, items, on_reorder=None, on_remove=None):
        super().__init__(parent)
        self.items = items
        self.labels = []
        self.drag_data = {"widget": None, "y": 0, "offset_y": 0, "index": None}
        self.drag_preview = None
        self.on_reorder = on_reorder
        self.on_remove = on_remove

        self.render()

    def render(self):
        # Clear old widgets
        for lbl in self.labels:
            lbl.destroy()
        self.labels.clear()

        self.grid_columnconfigure(0, weight=1)

        for i, item in enumerate(self.items):
            frame = ctk.CTkFrame(self)
            frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            frame.grid_columnconfigure(0, weight=1)

            lbl = ctk.CTkLabel(frame, text=item, fg_color="gray25", corner_radius=5, pady=5)
            lbl.grid(row=0, column=0, sticky="ew")

            lbl.bind("<ButtonPress-1>", self.on_start_drag)
            lbl.bind("<ButtonRelease-1>", self.on_drop)
            lbl.bind("<B1-Motion>", self.on_drag_motion)

            btn_remove = ctk.CTkButton(frame, text="−", width=25, command=lambda c=item: self.remove_item(c))
            btn_remove.grid(row=0, column=1, padx=5)

            self.labels.append(frame)

    def on_start_drag(self, event):
        widget = event.widget
        while widget not in self.labels and widget is not None:
            widget = widget.master
        if widget in self.labels:
            idx = self.labels.index(widget)
            self.drag_data["widget"] = widget
            self.drag_data["index"] = idx
            self.drag_data["y"] = event.y_root
            self.drag_data["offset_y"] = event.y

            # Create drag preview label (floating on top)
            text = self.items[idx]
            self.drag_preview = ctk.CTkLabel(self, text=text, fg_color="gray50", corner_radius=5, pady=5)
            self.drag_preview.place(in_=self, x=0, y=event.y_root - self.winfo_rooty() - self.drag_data["offset_y"], relwidth=1)

            # Hide original widget while dragging
            widget.grid_remove()
        else:
            self.drag_data = {"widget": None, "y": 0, "offset_y": 0, "index": None}

    def on_drag_motion(self, event):
        if self.drag_data["widget"] is None or self.drag_preview is None:
            return

        # Move the drag preview label with the mouse
        y = event.y_root - self.winfo_rooty() - self.drag_data["offset_y"]
        self.drag_preview.place_configure(y=y)

    def on_drop(self, event):
        if self.drag_data["widget"] is None or self.drag_preview is None:
            return

        # Find where to drop by cursor position
        drop_idx = self.get_closest_widget_index(event.y_root)

        # If no widget found under cursor, put at end
        if drop_idx is None:
            drop_idx = len(self.items) - 1

        old_idx = self.drag_data["index"]
        if drop_idx != old_idx:
            # Move the dragged item to the drop position
            item = self.items.pop(old_idx)
            self.items.insert(drop_idx, item)
            if self.on_reorder:
                self.on_reorder(self.items)

        # Destroy drag preview and show original widget again
        self.drag_preview.destroy()
        self.drag_preview = None

        self.drag_data = {"widget": None, "y": 0, "offset_y": 0, "index": None}
        self.render()

    def remove_item(self, item):
        self.items.remove(item)
        self.render()
        if self.on_reorder:
            self.on_reorder(self.items)
        if self.on_remove:
            self.on_remove(item)

    def get_closest_widget_index(self, y_root):
        # Find widget whose vertical position contains the y_root coordinate
        for i, widget in enumerate(self.labels):
            y1 = widget.winfo_rooty()
            y2 = y1 + widget.winfo_height()
            if y1 <= y_root <= y2:
                return i
        # If cursor is above all widgets, return 0 (top)
        if y_root < self.labels[0].winfo_rooty():
            return 0
        # If cursor is below all widgets, return last index
        if y_root > self.labels[-1].winfo_rooty() + self.labels[-1].winfo_height():
            return len(self.labels) - 1
        return None

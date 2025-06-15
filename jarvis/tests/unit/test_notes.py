import unittest
import tkinter as tk
import customtkinter as ctk
from unittest.mock import Mock

from jarvis.ui.notes_panel import NotesPanel
from jarvis.ui.note_widget import Note

class TestNoteWidget(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.mock_remove = Mock()
        self.note = Note(self.root, remove_callback=self.mock_remove)

    def test_set_and_get_content(self):
        sample_text = "Test note content"
        self.note.text_widget.insert("1.0", sample_text)
        self.assertEqual(self.note.get_content(), sample_text)

    def test_toggle_bold_adds_and_removes_tag(self):
        self.note.text_widget.insert("1.0", "Hello World")
        self.note.text_widget.tag_add(tk.SEL, "1.0", "1.5")  # Select "Hello"

        # First call adds bold
        self.note.make_bold()
        tags = self.note.text_widget.tag_names("1.0")
        self.assertIn("bold", tags)

        # Second call removes bold
        self.note.make_bold()
        tags = self.note.text_widget.tag_names("1.0")
        self.assertNotIn("bold", tags)

class TestNotesPanel(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.panel = NotesPanel(self.root)

    def test_add_note(self):
        self.panel.add_note()
        self.assertEqual(len(self.panel.notes), 1)
        self.assertIsInstance(self.panel.notes[0], Note)

    def test_remove_note(self):
        self.panel.add_note()
        note = self.panel.notes[0]
        self.panel.remove_note(note)
        self.assertEqual(len(self.panel.notes), 0)

    def test_save_notes_only_persistent(self):
        self.panel.add_note()
        self.panel.notes[0].text_widget.insert("1.0", "Persistent Note")
        self.panel.notes[0].is_persistent.set(True)

        self.panel.add_note()
        self.panel.notes[1].text_widget.insert("1.0", "Non Persistent Note")
        self.panel.notes[1].is_persistent.set(False)

        with self.assertLogs() as captured:
            self.panel.save_notes()
            # Confirm only 1 persistent note is printed
            self.assertIn("Persistent Note", captured.output[0])
            self.assertNotIn("Non Persistent Note", captured.output[0])

    def test_mousewheel_scroll_does_not_crash(self):
        try:
            # Simulate mouse wheel event
            event = Mock()
            event.delta = 120
            self.panel._on_mousewheel(event)
        except Exception as e:
            self.fail(f"Mousewheel scroll raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
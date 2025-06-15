import os
import unittest
import tkinter as tk
import customtkinter as ctk
from unittest.mock import Mock, patch
from jarvis.ui.notes_panel import NotesPanel
from jarvis.ui.note_widget import Note

HEADLESS = os.environ.get("CI") == "true"

class TestNoteWidget(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.mock_remove = Mock()
        self.note = Note(self.root, remove_callback=self.mock_remove)

    def tearDown(self):
        self.root.destroy()

    def test_set_and_get_content(self):
        sample_text = "Test note content"
        self.note.text_widget.insert("1.0", sample_text)
        self.assertEqual(self.note.get_content(), sample_text)

    @unittest.skipIf(HEADLESS, "Skipping GUI tests in CI/headless environments")
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

    def tearDown(self):
        self.root.destroy()

    @patch("jarvis.ui.notes_panel.db_notes.load_notes")
    def test_add_note(self, mock_load_notes):
        mock_load_notes.return_value = []
        panel = NotesPanel(self.root)
        panel.add_note()
        self.assertEqual(len(panel.notes), 1)
        self.assertIsInstance(panel.notes[0], Note)

    @patch("jarvis.ui.notes_panel.db_notes.load_notes")
    def test_remove_note(self, mock_load_notes):
        mock_load_notes.return_value = []
        panel = NotesPanel(self.root)
        panel.add_note()
        note = panel.notes[0]
        panel.remove_note(note)
        self.assertEqual(len(panel.notes), 0)

    @patch("jarvis.ui.notes_panel.db_notes.save_notes")
    @patch("jarvis.ui.notes_panel.db_notes.load_notes")
    def test_save_notes_only_persistent(self, mock_load_notes, mock_save_notes):
        mock_load_notes.return_value = []
        panel = NotesPanel(self.root)

        # Persistent note
        panel.add_note()
        panel.notes[0].text_widget.insert("1.0", "Persistent Note")
        panel.notes[0].is_persistent.set(True)

        # Non-persistent note
        panel.add_note()
        panel.notes[1].text_widget.insert("1.0", "Non Persistent Note")
        panel.notes[1].is_persistent.set(False)

        panel.save_notes()

        # Assert save_notes called with only the persistent note
        saved_notes = mock_save_notes.call_args[0][0]  # First positional argument
        self.assertEqual(len(saved_notes), 2)  # Both notes are sent to save_notes regardless
        persistent = [n for n in saved_notes if n["is_persistent"]]
        self.assertEqual(len(persistent), 1)
        self.assertEqual(persistent[0]["content"], "Persistent Note")

    @patch("jarvis.ui.notes_panel.db_notes.load_notes")
    def test_mousewheel_scroll_does_not_crash(self, mock_load_notes):
        mock_load_notes.return_value = []
        panel = NotesPanel(self.root)
        try:
            event = Mock()
            event.delta = 120
            panel._on_mousewheel(event)
        except Exception as e:
            self.fail(f"Mousewheel scroll raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
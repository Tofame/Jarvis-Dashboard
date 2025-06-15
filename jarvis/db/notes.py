from .session import SessionLocal
from .models import NoteModel

def save_notes(notes, overwrite=False):
    session = SessionLocal()
    try:
        if overwrite:
            session.query(NoteModel).delete()

        for note_dict in notes:
            # Don't save notes that aren't persistent
            if not note_dict.get("is_persistent", True):
                continue

            note = NoteModel(
                content=note_dict["content"],
                bg_color=note_dict.get("bg_color", "#fef3c7"),
                formatting=note_dict.get("formatting")
            )
            session.add(note)

        session.commit()
    finally:
        session.close()

def load_notes():
    session = SessionLocal()
    try:
        return session.query(NoteModel).all()
    finally:
        session.close()

def delete_note(note_id):
    session = SessionLocal()
    try:
        note = session.query(NoteModel).filter_by(id=note_id).first()
        if note:
            session.delete(note)
            session.commit()
    finally:
        session.close()
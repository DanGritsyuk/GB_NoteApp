from Model.Notes.Note import Note

class NoteComparatorByUpdateDate:
    @staticmethod
    def compare_notes_by_updated_date(note: Note) -> int:
        return note.updated
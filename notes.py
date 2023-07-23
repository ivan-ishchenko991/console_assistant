import json
from pathlib import Path
from abc import ABCMeta, abstractmethod


class AbstractNotes(metaclass=ABCMeta):
    @abstractmethod
    def add_note(self):
        pass

    @abstractmethod
    def search_notes(self):
        pass

    @abstractmethod
    def save_notes(self):
        pass

    @abstractmethod
    def load_notes(self):
        pass

    @abstractmethod
    def delete_note(self):
        pass

    @abstractmethod
    def edit_note(self):
        pass

    @abstractmethod
    def search_notes_by_tags(self):
        pass

    @abstractmethod
    def sort_notes_by_tags(self):
        pass

class Note:
    def __init__(self, title, text, tags=None):
        self.title = title
        self.text = text
        self.tags = tags


class Notebook(AbstractNotes):
    def __init__(self):
        self.notes = []

    dir_path = Path(__file__).parent
    
# Додавання нотаток
    def add_note(self, note):
        self.notes.append(note)


# Пошук нотаток за ключовим словом
    def search_notes(self, keyword):
        results = []
        for note in self.notes:
            if keyword in note.title or keyword in note.text or keyword in note.tags:
                results.append(note)
        return results


# Збереження нотаток у файл
    def save_notes(self, file_name):
        data = []
        for note in self.notes:
            data.append({
                'title': note.title,
                'text': note.text,
                'tags': note.tags
            })
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)


# Завантаження нотаток з файлу
    def load_notes(self, file_name):
        with open(fr'{Notebook.dir_path}\{file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                note = Note(item['title'], item['text'], item['tags'])
                self.add_note(note)

# Видалення нотатки
    def delete_note(self, note):
        self.notes.remove(note)


# Редагування нотатки
    def edit_note(self, note_title, new_title, new_text):
        for note in self.notes:
            if note.title == note_title:
                note.title = new_title
                note.text = new_text
                return True
        return False


# Пошук нотаток за тегами
    def search_notes_by_tags(self, tags):
        results = []
        for note in self.notes:
            if all(tag in note.tags for tag in tags):
                results.append(note)
        return results


# Сортування нотаток за тегами
    def sort_notes_by_tags(self):
        self.notes.sort(key=lambda note: note.tags)
import sys
from pathlib import Path
import shutil
import os
from abc import ABCMeta, abstractmethod


class AbstractSorter(metaclass=ABCMeta):
    @abstractmethod
    def create_folders(self):
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def sort_files(self):
        pass

class FileSorter(AbstractSorter):
    def __init__(self, folder):
        self.folder = folder
        self.name_folders = {
            ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'xls'): 'documents',
            ('png', 'jpg', 'jpeg', 'svg'): 'images',
            ('mp3', 'wav', 'amr', 'ogg'): 'audio',
            ('mp4', 'avi', 'mov', 'mkv'): 'video',
            ('zip', 'gz', 'tar'): 'archive'
        }

    def create_folders(self):
        folder_names = ['images', 'video', 'documents', 'audio', 'archive']

        for folder_name in folder_names:
            folder_path = os.path.join(self.folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def normalize(name):
        last_dot_index = name.rfind('.')
        CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                       "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

        TRANS = {}
        res = ''

        for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.upper()

        for i in name.translate(TRANS)[:last_dot_index]:
            if i.isalpha() or i.isdigit():
                res += i
            else:
                res += '_'

        return res + name[last_dot_index:]

    def sort_files(self):
        folders = []
        files = []

        if os.path.exists(self.folder):
            for dirpath, dirnames, filenames in os.walk(self.folder):
                for file in filenames:
                    files.append(os.path.join(dirpath, file))

                for folderr in dirnames:
                    folders.append(os.path.join(dirpath, folderr))

        for fl in files:
            new_name = self.normalize(os.path.basename(fl))
            path_drctr = os.path.join(self.folder, new_name)
            os.rename(fl, path_drctr)

        for dirpath, dirnames, filenames in os.walk(self.folder, topdown=False):
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                if not os.listdir(full_path):
                    os.rmdir(full_path)

        self.create_folders()

        for i in files:
            for key, value in self.name_folders.items():
                if i.lower().endswith(key):
                    filee = self.normalize(os.path.basename(i))
                    if value == 'archive':
                        last_dot_index = filee.rfind('.')
                        folder_path = os.path.join(
                            f'{self.folder}\\archive', filee[:last_dot_index])
                        shutil.unpack_archive(
                            f'{self.folder}\{filee}', folder_path)
                        os.remove(f'{self.folder}\{filee}')
                    else:
                        shutil.move(f'{self.folder}\{filee}',
                                    f'{self.folder}\{value}\{filee}')


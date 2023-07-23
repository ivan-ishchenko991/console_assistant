from address_book import AddressBook
from sort_folder import FileSorter
from pathlib import Path
from notes import Note, Notebook
from commands_docs import display_documentation
from prompt_toolkit import prompt
from commands_t9 import *
from weather import weather


#функція з кодом
def work_func():
    #об'єкт класу AddressBook
    ab = AddressBook()

    print(PREVIEW)
    #основний цикл програми
    while True:
        print('--------------------------\ninfo - вивід всіх команд\nexit - закінчення програми')
        ff = prompt('Enter the command: ', completer=commands_at_statup)

    #закінчення програми    
        if ff == 'exit':
            print('Good Bye!')
            break

    #інформація про всі команди    
        if ff == 'info':
            display_documentation()

    #перша команда, яка відповідає за адресну книгу    
        if ff == 'address book':
            if Path(ab.filename).exists():
                ab.unpackaging()
    
    
    #цикл команд з додавання, пошуку, редагування та видалення контакту           
            while True:
                command = prompt('Enter the command: ', completer=commands_for_the_ab)

                if command == 'exit':
                    ab.packaging()
                    break
                
                if command == 'add contact':
                    name = input("Enter a name: ")
                    address = input('Enter the address: ')
                    email = input("Enter email: ")
                    number = input("Ener the number: ")
                    birthday = input('Enter your date of birth: ')
                    ab.add_contact(name, address, email, number, birthday)
                    
                if command == 'birthday':
                    days = input('Enter the number of days: ')
                    ab.days_to_bday(days)
                    
                if command == 'search contact':
                    name_contact = input("Enter a contact's name to search: ")
                    ab.search_contacts(name_contact)
                
                if command == 'edit contact':
                    name_cont = input("Enter a contact for changes: ")
                    edit_value = input("enter something you want to change: ")
                    new_value = input("Enter a new value: ")
                    
                    ab.edit_contact(name_cont, edit_value, new_value)
                
                if command == 'delete contact':
                    delete_name = input("Enter the contact to delete: ")
                    ab.delete_contact(delete_name)
                
            
    #друга команда, яка відповідає за додаваня, пошук по слова і тегах, редагування, видалення, сортування та вивід нотаток              
        if ff == 'notes':
            notebook = Notebook()
            
            if Path(fr'{ab.dir_path}\notes.json').exists():
                notebook.load_notes("notes.json")
                
            while True:
                commandd = prompt('Enter the command: ', completer=commands_for_notes)
                
                if commandd == 'exit':
                    notebook.save_notes(fr'{ab.dir_path}\notes.json')
                    break
                
                if commandd == 'add note':
                    title = input("Enter a title: ")
                    text = input("Enter a text: ")
                    tags = input("Enter a tag: ")
                    new_note = Note(title, text, tags)
                    notebook.add_note(new_note)
                    
                if commandd == 'search':
                    sh_words = input('Enter a note to search for: ')
                    results = notebook.search_notes(sh_words)
                    for note in results:
                        print(note.title)
                        
                if commandd == 'edit':
                    note_ed = input('Enter a note to change the shift: ')
                    new_title = input('Enter a title: ')
                    new_text = input('Enter a text: ')
                    

                    if notebook.edit_note(note_ed, new_title, new_text):
                        print("The note was edited successfully")
                    else:
                        print("No note with this name was found")
                        
                if commandd == 'show all':
                    for note in notebook.notes:
                        print(note.title, "-", note.text)
                        
                if commandd == 'search by tags':
                    tag = input('Enter a tag: ')
                    results = notebook.search_notes_by_tags([tag])
                    for note in results:
                        print(note.title, "-", note.text)
                
                if commandd == 'sort by tags':
                    notebook.sort_notes_by_tags()
                
                if commandd == 'delete':
                    wordss = input('Enter a note to delete ')
                    del_note = notebook.search_notes(wordss)
                    if len(del_note) == 1:
                        notebook.delete_note(del_note[0])
                    else:
                        for note in del_note:
                            print(note.title, "-", note.text)
                        note_number = int(input('Enter a note number witch you want to delete: '))
                        notebook.delete_note(del_note[note_number - 1])
                
    
    #третя команда, яка відповідає за пошук погоди у введеному місті
        if ff == 'weather':
                while True:
                    commanddd = prompt('Enter the command: ', completer=commands_for_weather)
                    if commanddd == 'get weather':
                        weather()       
                        
                    if commanddd == 'exit':
                        break
                    
    #четверта команда, яка відповідає за сортування папки                
        if ff == 'sort folder':
            while True:
                commandddd = prompt('Enter the command: ', completer=commands_for_sf)
                
                if commandddd == 'exit':
                    break 
                
                if commandddd == 'sort folder':
                    path = input('Enter the folder path: ')
                    folder = Path(path)
                    file_sorter = FileSorter(folder)
                    file_sorter.sort_files()
                    print('Sorting completed!')
            

def main():
    work_func()

#виклик при запуску
if __name__ == '__main__':
    main()
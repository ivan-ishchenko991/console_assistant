import re
from datetime import datetime
import json
from pathlib import Path
from abc import abstractmethod, ABCMeta


# 1) зберігати контакти з іменами, адресами, номерами телефонів, email та днями 
# народження до книги контактів;

class AbstractBook(metaclass=ABCMeta):
    @abstractmethod
    def unpackaging(self):
        pass

    @abstractmethod
    def packaging(self):
        pass

    @abstractmethod
    def input_error(self):
        pass

    @abstractmethod
    def days_to_bday(self):
        pass

    @abstractmethod
    def search_contacts(self):
        pass

    @abstractmethod
    def add_contact(self):
        pass

    @abstractmethod
    def edit_contact(self):
        pass

    @abstractmethod
    def delete_contact(self):
        pass

    @abstractmethod
    def validate_phone_number(self):
        pass

    @abstractmethod
    def validate_email(self):
        pass

    @abstractmethod
    def validate_birthday(self):
        pass

class AddressBook(AbstractBook):
    contacts = {}

    dir_path = Path(__file__).parent
    filename = Path(fr'{dir_path}\addressbook.json')

    def unpackaging(self):
        with open(AddressBook.filename, 'r') as f:
            AddressBook.contacts.update(json.load(f))
    
    def packaging(self):
        with open(AddressBook.filename, 'w') as f:
            json.dump(AddressBook.contacts, f, indent=4)

    def input_error(func):
        def inner(*args):
            try:
                return func(*args)
            except (KeyError, ValueError, IndexError):
                print('\nCommand was entered incorrectly, please try again.\n') 
        return inner

# 2) виводити список контактів, у яких день народження через задану кількість 
#днів від поточної дати;

    def days_to_bday(self, n):

        if n.isdigit():
            BDAY_REGEX = re.compile(r"\d{2}\.\d{2}\.\d{4}")
            for name, args in self.contacts.items():
                for date in args:
                    if re.search(BDAY_REGEX, date):
                        d, m, y = date.split('.')
                        now = datetime.now()
                        some_day = datetime(year=now.year, month=int(m), day=int(d))
                        diff = some_day - now
                        if diff.days <= int(n) and diff.days >= 0:
                            print(f"{name}: {', '.join(args)}")
        else:
            print("Invalid value. Please write only a number.")

# 3) здійснення пошуку контактів серед контактів книги;

    def search_contacts(self, search_term=''):
        print("Search results:")
        for name, args in self.contacts.items():  # Додала цикл по елементам словника
            if search_term.lower() in name.lower() or \
                    any(search_term.lower() in arg.lower() for arg in args):
                print("Name: {}".format(name)) 
                print("Details: {}".format(', '.join(args)))
                print("---")

# 4) додавання та перевірка на правильність введеного номера телефону, email та дати народженняпід час створення, або редагування запису та повідомляти користувача у разі 
# некоректного введення;

    def add_contact(self, name, address, email, number, birthday):
        if not number:
            number = '-'
        else:
            if not self.validate_phone_number(number):
                print("Invalid number. Please check the format and try again.")
                return
            
        if not email:
            email = '-'
        else:
            if not self.validate_email(email):
                print("Invalid email. Please check the format and try again.")
                return
            
        if not birthday:
            birthday = '-'
        else:
            if not self.validate_birthday(birthday):
                print("Invalid date of birth. Please, use this format: day.month.year")
                return
        
        if not address:
            address = '-'

        self.contacts[name] = [address, email, number, birthday]
        print("Contact successfully added!")


#редагування контакту
    def edit_contact(self, name=None, arg=None, new_value=None):
        if name not in self.contacts:
            print("Contact not found.")
            return
        
        if arg == 'address':
            self.contacts[name][0] = new_value
            print("Contact successfully edited!")

        if arg == 'number':
            if not self.validate_phone_number(new_value):
                print("Invalid number. Please check the format and try again.")
                return
            self.contacts[name][2] = new_value
            print("Contact successfully edited!")

        if arg == 'email':
            if not self.validate_email(new_value):
                print("Invalid email. Please check the format and try again.")
                return
            self.contacts[name][1] = new_value
            print("Contact successfully edited!")

        if arg == 'birthday':
            if not self.validate_birthday(new_value):
                print("Invalid date of birth. Please, use this format: day.month.year")
                return          
            self.contacts[name][3] = new_value
            print("Contact successfully edited!")


#видалення контакту
    def delete_contact(self, name):
        if name not in self.contacts:
            print("Contact not found.")
            return

        del self.contacts[name]
        print("Contact successfully deleted!")

#паттерни і методи для перевірки правильності введення
    number_pattern = re.compile(r"\+?\(?(\d{2})?\)?\-?\(?(0\d{2})\)?\-?\d{3}\-?\d{2}\-?\d{2}")
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    birthday_pattern = r"\d{2}\.\d{2}\.\d{4}" 

    def validate_phone_number(self, phone_number):
        return bool(re.match(self.number_pattern, phone_number))

    def validate_email(self, email):
        return bool(re.match(self.email_pattern, email))
    
    def validate_birthday(self, birthday):
        return bool(re.match(self.birthday_pattern, birthday))
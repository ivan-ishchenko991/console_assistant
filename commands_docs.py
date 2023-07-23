def display_documentation():
    documentation = """
    address book - надає доступ до наступних команд
    add contact - додавання контакту у книгу
    birthday - вивід списку контактів, у яких день народження через задану кількість днів від поточної дати
    search contact - пошук контакту по імені
    edit contact - зміна контакту email, number, adress, birthday
    delete contact - видалення контакту
    exit - вихід з цієї команди

    notes - надає доступ до наступних команд
    add note - додавання нотаток 
    search - пошук нотатків за словами
    edit - зміна нотатки за title
    show all - вивід всіх нотатків
    sort by tags - сортування за тегами
    delete - видалення нотатки
    exit - вихід з цієї команди

    sort folder - надає доступ до наступних команд
    sort folder - сортування папки
    exit - вихід з цієї команди
    
    weather - надає доступ до наступних команд
    get weather - виводить погоду у введеному місті
    exit - вихід з цієї команди
    """

    # Виведення документації з відступами
    lines = documentation.strip().split('\n')
    formatted_documentation = '\n'.join('    ' + line.strip() for line in lines)
    print(formatted_documentation)

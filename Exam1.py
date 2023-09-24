# Реализовать консольное приложение заметки, с сохранением, чтением,
# добавлением, редактированием и удалением заметок. Заметка должна
# содержать идентификатор, заголовок, тело заметки и дату/время создания или
# последнего изменения заметки. Сохранение заметок необходимо сделать в
# формате json или csv формат (разделение полей рекомендуется делать через
# точку с запятой). Реализацию пользовательского интерфейса студент может
# делать как ему удобнее, можно делать как параметры запуска программы
# (команда, данные), можно делать как запрос команды с консоли и
# последующим вводом данных, как-то ещё, на усмотрение студента.



import json
import datetime
import argparse


def add_note(title, message, notes):
    note_id = len(notes) + 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = {
        'id': note_id,
        'заголовок': title,
        'сообщение': message,
        'дата/время': timestamp
    }
    notes.append(note)
    return notes


def delete_note(note_id, notes):
    filtered_notes = [note for note in notes if note['id'] != note_id]
    return filtered_notes


def edit_note(note_id, title, message, notes):
    for note in notes:
        if note['id'] == note_id:
            note['заголовок'] = title
            note['сообщение'] = message
            note['дата/время'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return notes


def filter_notes_by_date(start_date, end_date, notes):
    filtered_notes = [note for note in notes if start_date <= note['дата/время'] <= end_date]
    return filtered_notes


def save_notes_to_json(notes):
    with open('notes.json', 'w') as file:
        json.dump(notes, file)


def load_notes_from_json():
    try:
        with open('notes.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


parser = argparse.ArgumentParser(prog='notes', description='Консольное приложение для ведения заметок')
subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

add_parser = subparsers.add_parser('add', help='Добавьте новую заметку')
add_parser.add_argument('--заголовок', required=True, help='Название заметки')
add_parser.add_argument('--msg', required=True, help='Содержание записки')

delete_parser = subparsers.add_parser('delete', help='Удалить заметку')
delete_parser.add_argument('id', type=int, help='Идентификатор заметки, которую нужно удалить')

edit_parser = subparsers.add_parser('edit', help='Отредактируйте существующую заметку')
edit_parser.add_argument('id', type=int, help='Идентификатор заметки для редактирования')
edit_parser.add_argument('--заголовок', help='Новое название заметки')
edit_parser.add_argument('--msg', help='Новое сообщение в записке')

filter_parser = subparsers.add_parser('filter', help='Фильтровать заметки по дате')
filter_parser.add_argument('start_date', help='Дата начала (YYYY-MM-DD) фильтрации')
filter_parser.add_argument('end_date', help='Дата окончания (YYYY-MM-DD) фильтрации')

args = parser.parse_args()

if args.command == 'add':
    notes = load_notes_from_json()
    notes = add_note(args.title, args.msg, notes)
    save_notes_to_json(notes)
    print('Заметка успешно сохранена.')

elif args.command == 'delete':
    notes = load_notes_from_json()
    notes = delete_note(args.id, notes)
    save_notes_to_json(notes)
    print('Заметка успешно удалена.')

elif args.command == 'edit':
    notes = load_notes_from_json()
    notes = edit_note(args.id, args.title, args.msg, notes)
    save_notes_to_json(notes)
    print('Заметка успешно отредактирована.')

elif args.command == 'filter':
    notes = load_notes_from_json()
    filtered_notes = filter_notes_by_date(args.start_date, args.end_date, notes)
    for note in filtered_notes:
        print(f"ID: {note['id']}")
        print(f"Заголовок: {note['заголовок']}")
        print(f"Сообщение: {note['сообщение']}")
        print(f"Дата/время: {note['дата/время']}")
        print()

else:
    print('Команда не распознана.')
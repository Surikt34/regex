import csv
import re

def read_data(filename):
    with open(filename) as f:
        rows = csv.reader(f, delimiter=",")
        return list(rows)

def format_phone_numbers(contacts_list):
    pattern_number = r'(\+7|8)\s*(\(?)(\d{3})(\)?)\s*\-?(\d{3})[-\s*](\d{2})[-\s*]?(\d+)(\s*\(?доб.\s*(\d+)\)?)?'
    replacement_number = r'+7(\3)\5-\6-\7 \9'
    for sublist in contacts_list:
        sublist[-2] = re.sub(pattern_number, replacement_number, sublist[-2]).strip()
    return contacts_list

def split_fio(entry):
    fio_parts = entry[0].split() if ' ' in entry[0] else entry[:3]
    return fio_parts + entry[1:]

def combine_duplicates(contacts_list):
    unique_records = {}
    for record in contacts_list:
        key = (record[0], record[1])  # Фамилия и Имя как ключ
        if key not in unique_records:
            unique_records[key] = record
        else:
            for i in range(2, len(record)):
                if record[i]:
                    unique_records[key][i] = record[i]
    return list(unique_records.values())

def write_data(filename, contacts_list):
    with open(filename, "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


contacts_list = read_data("phonebook_raw.csv")
contacts_list = format_phone_numbers(contacts_list)
processed_data = [split_fio(entry) for entry in contacts_list[1:]]
final_data = [contacts_list[0]] + combine_duplicates(processed_data)
write_data("phonebook.csv", final_data)

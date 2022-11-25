import csv
import re
import prettytable
from prettytable import PrettyTable

def csv_reader(file_name):
    headlines_list = []
    vacancies_list = []
    length = 0
    first_element = True
    rows_count = 0
    with open(file_name, encoding="utf-8-sig") as File:
        reader = csv.reader(File)
        for row in reader:
            rows_count += 1
            if first_element:
                headlines_list = row
                length = len(row)
                first_element = False
            else:
                need_to_break = False
                if length != len(row):
                    need_to_break = True
                for word in row:
                    if word == "":
                        need_to_break = True
                if need_to_break:
                    continue
                vacancies_list.append(row)
    if rows_count == 0:
        print("Пустой файл")
        exit()
    if rows_count == 1:
        print("Нет данных")
        exit()
    return headlines_list, vacancies_list

def check_parametres():
    naming = ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы", "Премиум-вакансия",
                                     "Идентификатор валюты оклада", "Название", "Название региона", "Компания", ""]
    if len(filter_attribute) == 1 and filter_attribute[0] != "":
        print("Формат ввода некорректен")
        exit()
    elif filter_attribute[0] not in naming:
        print("Параметр поиска некорректен")
        exit()
    elif sort_property not in naming:
        print("Параметр сортировки некорректен")
        exit()
    elif is_reversed != "Да" and is_reversed != "Нет" and is_reversed != "":
        print("Порядок сортировки задан некорректно")
        exit()


def csv_filer(reader, list_naming):
    dictionaries_list = []
    for vacancy in reader:
        dictionary = {}
        for i in range(len(list_naming)):
            dictionary[list_naming[i]] = word_refactoring(vacancy[i])
        dictionaries_list.append(dictionary)
    return dictionaries_list


def cut_table(table, start_and_end, headlines, count):
    start = 0
    end = count
    start_and_end = start_and_end.split(" ")
    if start_and_end[0] == "":
        pass
    elif len(start_and_end) == 1:
        start = int(start_and_end[0]) - 1
    elif len(start_and_end) == 2:
        start = int(start_and_end[0]) - 1
        end = int(start_and_end[1]) - 1
    headlines = headlines.split(", ")
    if headlines[0] == "":
        return table.get_string(start=start, end=end)
    headlines.insert(0, "№")
    return table.get_string(start=start, end=end, ﬁelds=headlines)


def formatter(row):
    result_dictionary = {}
    min_salary = ""
    max_salary = ""
    before_taxes = ""
    for key in row:
        if key == "Нижняя граница вилки оклада":
            min_salary = number_refactoring(str(int(float(row[key]))))
        elif key == "Верхняя граница вилки оклада":
            max_salary = number_refactoring(str(int(float(row[key]))))
        elif key == "Оклад указан до вычета налогов":
            before_taxes = ("Без вычета налогов" if row[key] == "Да" else "С вычетом налогов")
        elif key == "Идентификатор валюты оклада":
            result_dictionary["Оклад"] = f"{min_salary} - {max_salary} ({row[key]}) ({before_taxes})"
        elif key == "Дата публикации вакансии":
            result_dictionary[key] = row[key][8: 10] + "." + row[key][5: 7] + "." + row[key][: 4]
        else:
            result_dictionary[key] = row[key]
    return result_dictionary


def filter_rows(dictionary, filter):
    filter = filter.split(": ")
    naming = ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы", "Премиум-вакансия",
              "Идентификатор валюты оклада", "Название", "Название региона", "Компания", ""]
    if len(filter) == 1 and filter[0] != "":
        print("Формат ввода некорректен")
        exit()
    elif filter[0] not in naming:
        print("Параметр поиска некорректен")
        exit()
    for key in dictionary:
        if filter[0] == "Оклад":
            if key == "Нижняя граница вилки оклада":
                if int(float(filter[1])) < int(float(dictionary[key])):
                    return False
            elif key == "Верхняя граница вилки оклада":
                if int(float(filter[1])) > int(float(dictionary[key])):
                    return False
        elif filter[0] == "Дата публикации вакансии" == key:
            if filter[1] != dictionary[key][8: 10] + "." + dictionary[key][5: 7] + "." + dictionary[key][: 4]:
                return False
        elif filter[0] == key == "Навыки":
            for element in filter[1].split(", "):
                if element not in dictionary[key].split("\n"):
                    return False
        elif filter[0] == key:
            if filter[1] != dictionary[key]:
                return False
    return True


def sort_vacancies(data_vacancies, attribute, is_reversed):
    is_reversed = (True if is_reversed == "Да" else False)
    if attribute == "":
        sorted_vacancies = data_vacancies
    elif attribute == "Навыки":
        sorted_vacancies = sorted(data_vacancies, key=lambda dictionary:
            len(dictionary[attribute].split("\n")), reverse=is_reversed)
    elif attribute == "Оклад":
        sorted_vacancies = sorted(data_vacancies,
                                  key=lambda dictionary: (int(float(dictionary["Нижняя граница вилки оклада"])) +
                                                          int(float(dictionary["Верхняя граница вилки оклада"]))) *
                                                         dict_currencies[dictionary["Идентификатор валюты оклада"]],
                                                        reverse=is_reversed)
    elif attribute == "Опыт работы":
        expirience_dictionary = {"Нет опыта": 0, "От 1 года до 3 лет": 1, "От 3 до 6 лет": 2, "Более 6 лет": 3}
        sorted_vacancies = sorted(data_vacancies, key=lambda dictionary:
                                  expirience_dictionary[dictionary[attribute]], reverse=is_reversed)
    else:
        sorted_vacancies = sorted(data_vacancies, key=lambda dictionary: dictionary[attribute], reverse=is_reversed)
    return sorted_vacancies


def print_vacancies(data_vacancies, dic_naming):
    table = PrettyTable(hrules=prettytable.ALL, align='l')
    is_first_row = True
    number = 0
    current_data_vacancies = sort_vacancies(({dic_naming[key]: dictionary[key] for key in dictionary} for dictionary in data_vacancies),
                                            sort_property, is_reversed)
    for current_dictionary in current_data_vacancies:
        formatted_current_dictionary = formatter(current_dictionary)
        if is_first_row:
            first_row = [key for key in formatted_current_dictionary]
            first_row.insert(0, "№")
            table.field_names = first_row
            is_first_row = False
            number += 1
        if not filter_rows(current_dictionary, filter):
            continue
        row = [value if len(value) <= 100 else value[:100] + "..." for value in formatted_current_dictionary.values()]
        row.insert(0, number)
        table.add_row(row)
        number += 1
    if number == 1:
        print("Ничего не найдено")
        exit()

    table.max_width = 20
    table = cut_table(table, diapason, columns, number - 1)
    print(table)

def number_refactoring(number):
    first_digit_count, triplets_count = len(number) % 3, len(number) // 3
    result_number = number[:first_digit_count]
    for i in range(triplets_count):
        if not (result_number == ""):
            result_number += " "
        result_number += number[first_digit_count + i * 3: first_digit_count + (i + 1) * 3]
    return result_number

def word_refactoring(string):
    refactored_string = re.compile(r'<[^>]+>').sub('', string)
    refactored_string = refactored_string.replace(" ", " ").replace(" ", " ").replace("  ", " ").replace(
        "  ", " ").strip()
    return dict_tranclator[refactored_string] if refactored_string in dict_tranclator else refactored_string


dict_tranclator = {"name": "Название",
              "description": "Описание",
              "key_skills": "Навыки",
              "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия",
              "employer_name": "Компания",
              "salary_from": "Нижняя граница вилки оклада",
              "salary_to": "Верхняя граница вилки оклада",
              "salary_gross": "Оклад указан до вычета налогов",
              "salary_currency": "Идентификатор валюты оклада",
              "area_name": "Название региона",
              "published_at": "Дата публикации вакансии",
              "noExperience": "Нет опыта",
              "between1And3": "От 1 года до 3 лет",
              "between3And6": "От 3 до 6 лет",
              "moreThan6": "Более 6 лет",
              "AZN": "Манаты",
              "BYR": "Белорусские рубли",
              "EUR": "Евро",
              "GEL": "Грузинский лари",
              "KGS": "Киргизский сом",
              "KZT": "Тенге",
              "RUR": "Рубли",
              "UAH": "Гривны",
              "USD": "Доллары",
              "UZS": "Узбекский сум",
              "True": "Да",
              "False": "Нет",
              "FALSE": "Нет",
              "TRUE": "Да"}

dict_currencies = {"Манаты": 35.68,
                   "Белорусские рубли": 23.91,
                   "Евро": 59.90,
                   "Грузинский лари": 21.74,
                   "Киргизский сом": 0.76,
                   "Тенге": 0.13,
                   "Рубли": 1,
                   "Гривны": 1.64,
                   "Доллары": 60.66,
                   "Узбекский сум": 0.0055, }

def get_pretty_table():
    global file_name
    global filter
    global sort_property
    global is_reversed
    global diapason
    global columns
    global filter_attribute
    file_name = input("Введите название файла: ")
    filter = input("Введите параметр фильтрации: ")
    sort_property = input("Введите параметр сортировки: ")
    is_reversed = input("Обратный порядок сортировки (Да / Нет): ")
    diapason = input("Введите диапазон вывода: ")
    columns = input("Введите требуемые столбцы: ")
    filter_attribute = filter.split(": ")
    check_parametres()
    headlines, vacancies = csv_reader(file_name)
    dictionaries_list = csv_filer(vacancies, headlines)
    print_vacancies(dictionaries_list, dict_tranclator)
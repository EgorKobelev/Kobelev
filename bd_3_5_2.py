import pandas as pd
import sqlite3


class BDFormatter:
    """
    Класс для преобразования csv-файла в бд с форматированием
    Attributes:
        con (Connection): соединение с бд
        file_name (string): название csv-файла для преобразования
        available_currencies (list): доступные валюты
    """
    def __init__(self, file_name):
        """
        Инициализирует класс DBFormatter
        Args:
            file_name (string): название csv-файла для преобразования
        """
        self.con = sqlite3.connect("currencies.db")
        self.file_name = file_name
        self.available_currencies = list(
            pd.read_sql("SELECT * from currencies WHERE date='2003-01'", self.con).keys()[1:])

    def csv_to_bd(self, file_name):
        """
        Преобразует csv-файл в бд
        Args:
            file_name (strng): название csv-файла для преобразования
        """
        df = pd.read_csv(file_name)
        con = sqlite3.connect('currencies.db')
        c = con.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS bd_3_5_2 (name text, area_name text, published_at text, salary number)')
        con.commit()
        df.to_sql('bd_3_5_2', con, if_exists='replace', index=False)

    def get_salary(self, row):
        """
        Производит конвертацию зарплат
        Args:
            row (DataFrame): строка в csv-файле для конвертации
        returns:
            float: конвертированная зарплата

        """
        salary_from, salary_to, salary_currency, published_at = str(row[0]), str(row[1]), str(row[2]), str(row[3])
        if salary_currency == 'nan':
            return 'nan'
        if salary_from != 'nan' and salary_to != 'nan':
            salary = float(salary_from) + float(salary_to)
        elif salary_from != 'nan' and salary_to == 'nan':
            salary = float(salary_from)
        elif salary_from == 'nan' and salary_to != 'nan':
            salary = float(salary_to)
        else:
            return 'nan'
        if salary_currency != 'RUR' and salary_currency in self.available_currencies:
            date = published_at[:7]
            try:
                multi = pd.read_sql(f"SELECT {salary_currency} from currencies WHERE date='{date}'", self.con)[
                    f'{salary_currency}'][0]
                if multi is not None:
                    salary *= multi
                return 'nan'
            except:
                return 'nan'
        return round(salary)

    def process_salaries(self):
        """
        Проходится по всему начальному csv-файлу, преобразую его. Создает новый csv-файла
        """
        df = pd.read_csv(self.file_name)
        df['salary'] = df[['salary_from', 'salary_to', 'salary_currency', 'published_at']].apply(self.get_salary,
                                                                                                 axis=1)
        df['published_at'] = df['published_at'].apply(lambda x: x[:7])
        df.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis=1, inplace=True)
        df.to_csv('vacancies_bd_3_5_2.csv', index=False)


sql_formatter = BDFormatter('vacancies_dif_currencies.csv')
sql_formatter.process_salaries()
sql_formatter.csv_to_bd('vacancies_bd_3_5_2.csv')

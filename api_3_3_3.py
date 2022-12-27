import pandas as pd
import requests
import json

pd.set_option("display.max_columns", None)


class hh_parser:
    """Класс для парсинга вакансий с hh
    Attributes:
        info (dict): словарь для формирования csv-файла с названием профессии, зарплатой, местностью и датой публикации
    """
    def __init__(self):
        """
        Инициализирует класс hh_parser
        """
        self.info = {'name': [], 'salary_from': [], 'salary_to': [], 'salary_currency': [], 'area_name': [],
                     'published_at': []}

    def get_data(self):
        """
        Запрашивает данные с сайта hh.ru и записывает их в словарь
        """
        for date_from in ['2022-12-20T00:00:00', '2022-12-20T06:00:00', '2022-12-20T12:00:00', '2022-12-20T18:00:00',
                          '2022-12-21T00:00:00']:
            date_to = '2022-12-21T00:00:00'
            for page in range(1, 20):
                request = requests.get(
                    f'https://api.hh.ru/vacancies?date_from={date_from}&date_to={date_to}&specialization=1&per_page=100&page={page}')
                for item in json.loads(request.text)['items']:
                    print(item)
                    self.info['name'].append(item['name'])
                    salary = item['salary']
                    salary_from, salary_to, salary_currency = None, None, None
                    if salary is not None:
                        salary_from = salary['from']
                        salary_to = salary['to']
                        salary_currency = salary['currency']
                    self.info['salary_from'].append(salary_from)
                    self.info['salary_to'].append(salary_to)
                    self.info['salary_currency'].append(salary_currency)
                    area = item['area']
                    area_name = None
                    if area is not None:
                        area_name = area['name']
                    self.info['area_name'].append(area_name)
                    self.info['published_at'].append(item['published_at'])

    def create_csv(self):
        """
        На основе сформированного словаря создает csv-файл
        """
        df = pd.DataFrame(self.info)
        df.to_csv('hh.csv')


parser = hh_parser()
parser.get_data()
parser.create_csv()
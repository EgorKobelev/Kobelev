import csv


class CsvCutter:
    """ Разделяет основной csv-файл на несколько маленьких по годам
    Attributes:
        file_name (string): название файла, с которым нужно провести операцию
        headers (list): заголовки
        info (dict): словарь - год : данные
    """
    def __init__(self, file_name):
        """ Инициализирует CsvCutter
        Args:
            file_name (string): название файла, с которым нужно провести операцию
        """
        self.file_name = file_name
        self.headers = []
        self.info = {}

    def separate_csv(self):
        """Создает csv-файлы по годам
        """
        for year in self.info:
            with open(f'csv_files/new_csv_{year}.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in self.info[year]:
                    filewriter.writerow(row)

    def read_file(self):
        """Читает основной csv-файл, записывая данные по годам в словарь
        """
        first_element = True
        with open(self.file_name, encoding="utf-8-sig") as File:
            reader = csv.reader(File)
            for row in reader:
                if first_element:
                    self.headers = row
                    first_element = False
                else:
                    if row[-1][:4] in self.info.keys():
                        self.info[row[-1][:4]].append(row)
                    else:
                        self.info[row[-1][:4]] = [self.headers, row]


csv_cutter = CsvCutter("vacancies_by_year.csv")
csv_cutter.read_file()
csv_cutter.separate_csv()

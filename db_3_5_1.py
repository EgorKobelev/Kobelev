import pandas as pd
import sqlite3


class DBConverter:
    """Класс для конвертации csv в db.
    Attributes:
        csv_path(str): путь до файла csv.
        db_name(str): название базы данных.
    """

    def __init__(self, csv_path: str, db_name: str):
        """Инициализация. создание базы данных из csv-файла.
        Args:
            csv_path(str): путь до файла csv.
            db_name(str): название базы данных.
        """
        self.csv_path = csv_path
        self.db_name = db_name
        self.create_db()

    def create_db(self):
        """Конверация csv с валютами в db с валютами."""
        con = sqlite3.connect(self.db_name)
        pd.read_csv(self.csv_path).to_sql("currencies", con, index=False, if_exists="replace")


converter = DBConverter("currencies.csv", "currencies.db")
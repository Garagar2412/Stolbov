import csv
from datetime import datetime

class SplitingCSV:
    """
        Класс для разделения данных из файла CSV.
        Attributes:
            file_name (str): Название CSV файла
        """

    def __init__(self, file_name):
        """
        Инициализирует объект SplitingCSV.
        Args:
            file_name (str): Название CSV файла
        """
        self.file_name = file_name

    def split_csv(self):
        """
        Разделяет файл CSV на несколько по годам.
        """
        years_list = []
        with open(self.file_name, newline='', encoding='utf-8-sig') as file:
            vacancies_csv = csv.reader(file)
            vacancy_data = [row for row in vacancies_csv]
            vacancy_keys = []
            try:
                vacancy_keys = vacancy_data.pop(0)
            except:
                print('Пустой файл')
                exit()
            index_date = vacancy_keys.index('published_at')
            filtered_vacancy_data = [vacancy for vacancy in vacancy_data
                                    if len(vacancy) == len(vacancy_keys) and '' not in vacancy]
            for vacancy in filtered_vacancy_data:
                year = datetime.strptime(vacancy[index_date], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y')
                if year not in years_list:
                    with open(f"{year}.csv", mode="w", encoding='utf-8-sig') as w_file:
                        file_writer = csv.writer(w_file, delimiter=',', lineterminator="\r")
                        years_list.append(year)
                        file_writer.writerow(vacancy_keys)
                        file_writer.writerow(vacancy)
                else:
                    with open(f"{year}.csv", mode="a", encoding='utf-8-sig') as w_file:
                        file_writer = csv.writer(w_file, delimiter=',', lineterminator="\r")
                        file_writer.writerow(vacancy)

def main():
    """Создает объект SplitingCSV, разделяет CSV файл."""
    a = SplitingCSV(input())
    a.split_csv()

if __name__ == '__main__':
    main()
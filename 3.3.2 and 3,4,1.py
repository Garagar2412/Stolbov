import numpy as np
import pandas as pd
from pathlib import Path
def formatter(file, curr_dict_date):
    """
    Форматирует зарплату вакансии: приводит ее к рублям и к среднему значению; создает датафреймы.
    :param file: Файл, из которого берутся вакансии
    :param curr_dict_date: Файл, в котором собраны курсы валют за определенный промежуток времени
    """
    vacancies = pd.read_csv(file,nrows=100)
    val_curs = pd.read_csv(curr_dict_date)
    val_curs.rename(columns={'Date': 'date'}, inplace=True)
    vacancies = vacancies.fillna(0)
    val_curs = val_curs.fillna(0)
    currencies = val_curs.columns.values[1:]
    vacancies.loc[((vacancies['salary_from'].astype(float) == 0) | (vacancies['salary_to'].astype(float) == 0)), 'salary_not_rur'] = \
        vacancies['salary_from'].astype(float) + vacancies['salary_to'].astype(float)
    vacancies.loc[((vacancies['salary_from'].astype(float) != 0) & (vacancies['salary_to'].astype(float) != 0)), 'salary_not_rur'] = \
        (vacancies['salary_from'].astype(float) + vacancies['salary_to'].astype(float)) / 2
    vacancies['date'] = vacancies['published_at'].str[:7]
    vacancies = pd.merge(vacancies, val_curs, how='left', on='date')
    vacancies['salary'] = np.nan
    for curr in list(currencies):
        vacancies.loc[vacancies['salary_currency'] == curr, 'salary'] = round(vacancies[curr] * vacancies['salary_not_rur'])
        vacancies.loc[vacancies[curr] == 0, 'salary'] = np.nan
    vacancies.loc[vacancies['salary_currency'] == 'RUR', 'salary'] = vacancies['salary_not_rur']
    vacancies['salary'] = vacancies['salary'].astype(float)
    new_vacancies = vacancies[['name', 'salary', 'area_name', 'published_at']]
    new_vacancies.to_csv('vacancy_100.csv', index=False)

def get_news_files():
    """
    Запускает форматирование вакансий из файлов, лежащих в определенной папке.
    """
    curr_dict_date = input('Файл с валютами: ')
    file_vac = input('Файл с вакансиями: ')
    formatter(file_vac, curr_dict_date)

if __name__ == '__main__':
    get_news_files()
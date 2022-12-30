import pandas as pd
import pdfkit
from jinja2 import Environment, FileSystemLoader

def get_dataframes(file, vacancy, area_name):
    """
    Создает датафреймы со статистикой по городам, по годам для определенной вакансии и региона.
    :param file: Файл с вакансиями
    :param vacancy: Название вакансии
    :param area_name: Название региона
    :return: датафреймы со статистикой по городам, по годам для определенной вакансии и региона
    """
    vacancies = pd.read_csv(file)
    vacancies_salary_city = round(vacancies[['area_name', 'salary']].groupby('area_name').mean())
    vacancies_count_city = vacancies.groupby('area_name')['name'].count()

    vacancies_city = pd.merge(vacancies_salary_city, vacancies_count_city, how='left', on='area_name')
    vacancies_sum = vacancies_city['name'].sum()
    vacancies_city = vacancies_city[vacancies_city['name'] / vacancies_sum >= 0.01]

    vacancies_salary_city_top = vacancies_city.reset_index(level=0)[['area_name', 'salary']].sort_values('salary', ascending=0)[['area_name', 'salary']].head(10)
    vacancies_salary_city_top.rename(columns={'area_name': 'Регион', 'salary': 'Средняя зарплата'}, inplace=True)

    vacancies_count_city_top = vacancies_city.reset_index(level=0)[['area_name', 'name']].sort_values('name', ascending=0)[['area_name', 'name']].head(10)
    vacancies_count_city_top.rename(columns={'area_name': 'Регион', 'name': 'Количество вакансий'}, inplace=True)

    vacancies['Год'] = vacancies['published_at'].str[:4]

    vacancy_salary = round(vacancies[(vacancies['name'].str.lower().str.contains(f'{vacancy}'.lower())) & (vacancies['area_name'].str.lower() == f'{area_name}'.lower())][['Год', 'salary']].groupby('Год').mean())
    vacancy_count = vacancies[(vacancies['name'].str.lower().str.contains(f'{vacancy}'.lower())) & (vacancies['area_name'].str.lower() == f'{area_name}'.lower())].groupby('Год')['name'].count()
    statistic_vacancy = pd.merge(vacancy_salary, vacancy_count, how='left', on='Год').fillna(0).astype(int)\
            .reset_index(level=0)
    statistic_vacancy.rename(columns={'salary': f'Средняя зарплата',
                                      'name': f'Количество вакансий'}, inplace=True)
    statistic_vacancy = pd.merge(pd.DataFrame({'Год': vacancies['Год'].unique()}), statistic_vacancy, how='left', on='Год').fillna(0).astype(int)
    return [vacancies_salary_city_top, vacancies_count_city_top, statistic_vacancy]

def get_pdf(dataframes, vacancy, area_name):
    """
    Создает html-страницу с датафреймом и конвертирует ее в пдф.
    :param dataframe: Датафрейм со статистикой
    """
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('city_statistic.html')
    pdf_template = template.render({'table0': dataframes[0].to_html(index=False),
                                    'table1': dataframes[1].to_html(index=False),
                                    'table2': dataframes[2].to_html(index=False),
                                    'vacancy': vacancy, 'area_name': area_name})
 
    config = pdfkit.configuration(wkhtmltopdf=r'D:\Games\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(pdf_template, 'statisticCityPandas.pdf',
                       configuration=config, options={"enable-local-file-access": ""})


if __name__ == '__main__':
    file = input('Введите название файла: ')
    vacancy = input('Введите название профессии: ')
    area_name = input('Введите название региона: ')
    # file = r'C:\Users\stolb\PycharmProjects\Stolbov\vacancies_dif_currencies.csv'
    # vacancy = 'программист'
    # area_name = 'Екатеринбург'
    get_pdf(get_dataframes(file, vacancy, area_name), vacancy, area_name)


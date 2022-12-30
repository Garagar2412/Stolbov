import pandas as pd
import requests
from datetime import datetime

pd.set_option("expand_frame_repr", False)

def get_request_dates(date: str):
    request_dates = []
    input_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    for i in range(4):
        request_dates.append(input_date.replace(hour=i * 6, minute=0, second=0).strftime('%Y-%m-%dT%H:%M:%S'))
    request_dates.append(input_date.replace(hour=23, minute=59, second=59).strftime('%Y-%m-%dT%H:%M:%S'))
    return request_dates

def get_json(page_number: int, start_date: str, end_date: str):
    while True:
        response = requests.get(
            f"https://api.hh.ru/vacancies?date_from={start_date}&date_to={end_date}&specialization=1&per_page=100&page={page_number}")
        if response.status_code == 200:
            return response.json()

def get_vacancies_info(start_date: str, end_date: str):
    vacancies_info = []
    response_json = requests.get(
        f"https://api.hh.ru/vacancies?date_from={start_date}&date_to={end_date}&specialization=1&per_page=100").json()
    pages = response_json["pages"]
    for page_number in range(pages):
        vacancies_info_page_json = get_json(page_number, start_date, end_date)
        for vacancy_info in vacancies_info_page_json["items"]:
            vacancies_info.append({
                "name": vacancy_info["name"],
                "salary_from": vacancy_info["salary"]["from"] if vacancy_info["salary"] else None,
                "salary_to": vacancy_info["salary"]["to"] if vacancy_info["salary"] else None,
                "salary_currency": vacancy_info["salary"]["currency"] if vacancy_info["salary"] else None,
                "area_name": vacancy_info["area"]["name"],
                "published_at": vacancy_info["published_at"]
            })
    return vacancies_info

def get_full_day_vacancies_info(request_dates: list[str]):
    if len(request_dates) == 0:
        return
    full_day_vacancies_info = []
    for i in range(1, len(request_dates)):
        full_day_vacancies_info += get_vacancies_info(request_dates[i - 1], request_dates[i])
    return full_day_vacancies_info


request_dates = get_request_dates('2022-12-12T12:12:12+0300')
vacancies_info = get_full_day_vacancies_info(request_dates)
df = pd.DataFrame.from_dict(vacancies_info)
df.to_csv("hh_api_vacancies.csv")
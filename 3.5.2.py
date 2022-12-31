import sqlite3
import pandas as pd
from statistics import mean
import math

currency_name_to_number = {
    "BYR": 1,
    "USD": 2,
    "EUR": 3,
    "KZT": 4,
    "UAH": 5
}

pd.set_option("expand_frame_repr", False)

#Обработка данных о зарплате
def handle_salary(date, salary_from, salary_to, salary_currency, cur):
    currency_exchange = 0
    if salary_currency in ["BYN", "BYR", "EUR", "KZT", "UAH", "USD"]:
        salary_currency.replace("BYN", "BYR")
        date = f"{date[1]}-{date[0]}"
        cur.execute("select * from currencies where date == :date", {"date": date})
    elif salary_currency == "RUR":
        currency_exchange = 1

    if not (math.isnan(salary_from)) and not (math.isnan(salary_to)):
        to_return_salary = mean([salary_from, salary_to]) * currency_exchange
    elif not (math.isnan(salary_from)):
        to_return_salary = salary_from * currency_exchange
    else:
        to_return_salary = salary_to * currency_exchange

    if math.isnan(to_return_salary):
        return to_return_salary
    return int(to_return_salary)


df = pd.read_csv("vacancies_dif_currencies (1).csv")
con = sqlite3.connect("currencies.db")
cur = con.cursor()

# Запись в отдельный столбец корректной информации о зарплате
df["salary"] = df.apply(lambda row:
                        handle_salary(row["published_at"][:7].split("-"),
                                      row["salary_from"],
                                      row["salary_to"],
                                      row["salary_currency"],
                                      cur),
                        axis=1)

# Приведение формата даты к указанному в задании
df["published_at"] = df.apply(lambda row: row["published_at"][0:7], axis=1)

# Удаление ненужных столбцов
df = df.drop(["salary_from", "salary_to", "salary_currency"], axis=1)

# Приведение порядка столбцов к указанному в задании
df = df.loc[:, ["name", "salary", "area_name", "published_at"]]

# Работа с базой данных
con = sqlite3.connect("vacancies.db")
df.to_sql("vacancies", con=con, if_exists="replace", index=False)
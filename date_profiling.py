import cProfile
import csv
import datefinder
from datetime import datetime


with open('vacancies_by_year.csv', 'r', encoding='utf-8-sig') as f:
	dates = [vacancy[-1] for vacancy in csv.reader(f)][1:]


def profile_it(func):
	def wrapper(date_list):
		profile = cProfile.Profile()
		profile.enable()
		f = [func(arg) for arg in date_list]
		profile.disable()
		print('Статистика по функции', func.__name__)
		profile.print_stats(0)

	return wrapper


'''def datetime_test(date):
	date = datetime.strptime(date[:10], '%Y-%m-%d').date()
	return f'{date.day}.{date.month}.{date.year}'
	'''


def slice_test(date):
	day = date[8:10]
	month = date[5:7]
	year = date[:4]
	return f'{day}.{month}.{year}'


'''def split_test(date):
	date = date.split('T')[0].split('-')
	day = date[2]
	month = date[1]
	year = date[0]
	return f'{day}.{month}.{year}'


def datefinder_test(date):
	matches = list(datefinder.find_dates(date))
	date = str(matches[0])
	return f'{date[8:10]}.{date[5:7]}.{date[:4]}'


def test_parsing_with_format(date):
	return '{0[2]}.{0[1]}.{0[0]}'.format(date[:10].split('-'))'''


if __name__ == '__main__':
	profiler_data = profile_it(slice_test)
	profiler_data(dates)
from unittest import TestCase, main
from main import Vacancy, Report, DataSet


class DataSetTest(TestCase):
	def test_dataset_type(self):
		self.assertEqual(type(DataSet('', '')).__name__, 'DataSet')
	def test_file_name(self):
		self.assertEqual(DataSet('vacancies.csv', 'Аналитик').file_name, 'vacancies.csv')
	def test_vacancy_name(self):
		self.assertEqual(DataSet('vacancies.csv', 'Аналитик').vacancy_name, 'Аналитик')
	def test_method_average(self):
		self.assertEqual(DataSet('', '').average({2007: [10000, 15000, 20000], 2008: [30000, 35000, 40000]}), {2007: 15000, 2008: 35000})


class ReportTest(TestCase):
	def test_wb_type(self):
		self.assertEqual(type(Report('', {}, {}, {}, {}, {}, {}).wb).__name__, 'Workbook')

	def report_test_any_stats(self):
		self.assertEqual(Report('', {}, {}, {}, {}, {}, {'Москва': 0.441, 'Санкт-Петербург': 0.223}).stats6['Москва'],
		                 0.441)

	def report_test_stats(self):
		self.assertEqual(Report('', {2007: 30000, 2008: 35000, 2009: 40000}, {}, {}, {}, {}, {}).stats1[2007], 30000)

	def report_test_type(self):
		self.assertEqual(type(Report('', {}, {}, {}, {}, {}, {})).__name__, 'Report')

	def report_test_vacancy_name(self):
		self.assertEqual(Report('Аналитик', {}, {}, {}, {}, {}, {}).vacancy_name, 'Аналитик')


vacancy_dct = {'name': 'Программист', 'salary_from': '150', 'salary_to': '200', 'salary_currency': 'RUR',
               'area_name': 'Екатеринбург', 'published_at': '2007-12-03T17:40:09+0300'}


class VacancyTest(TestCase):
	def test_vacancy_name(self):
		self.assertEqual(Vacancy(vacancy_dct).name, 'Программист')

	def test_vacancy_type(self):
		self.assertEqual(type(Vacancy(vacancy_dct)).__name__, 'Vacancy')

	def test_area_name(self):
		self.assertEqual(Vacancy(vacancy_dct).area_name, 'Екатеринбург')

	def test_vacancy_salary_to(self):
		self.assertEqual(Vacancy(vacancy_dct).salary_to, 200)

	def test_vacancy_salary_from(self):
		self.assertEqual(Vacancy(vacancy_dct).salary_from, 150)

	def test_vacancy_salary_currency(self):
		self.assertEqual(Vacancy(vacancy_dct).salary_currency, 'RUR')

	def test_vacancy_average_salary(self):
		self.assertEqual(Vacancy(vacancy_dct).salary_average, 175.0)

	def test_vacancy_year(self):
		self.assertEqual(Vacancy(vacancy_dct).year, 2007)


if __name__ == '__main__':
	main()
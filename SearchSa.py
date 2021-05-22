import pandas as pd
import re

heuristic = {
	# 'triệu': 1e6,
	'tr': 1e6,
	'usd': 23000,
	'$': 23000
}
replace_str = {
	',': '.',
	'-': ' ',
	'trên': '>',
	'dưới': '<',
	'từ': '>=',
	'tới': '<='
}


class SalaryManagement(object):
	def __init__(self, data):
		self.data = data

	def convert(self, text: str, heuristic: dict):
		text = text.lower()
		raw_text = text
		for char in replace_str.keys():
			text = text.replace(char, replace_str[char])
		numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
		is_change = False
		for key in heuristic.keys():
			if key in text:
				if key == 'usd' or '$':
					for i, _ in enumerate(numbers):
						_ = _.replace('.', '')
						numbers[i] = float(_) * heuristic[key]
				elif key == 'tr':
					numbers = [float(_) * heuristic[key] for _ in numbers]
				is_change = True

		if not is_change and len(numbers) > 1:
			temp_numbers = []
			if len(numbers) % 2 == 0:
				for i in range(0, len(numbers), 2):
					temp = numbers[i] + numbers[i + 1]
					temp_numbers.append(float(temp.replace('.', '')))
				numbers = temp_numbers
			else:
				number_1 = float(numbers[0])
				number_2 = (numbers[1] + numbers[2])
				number_1 = number_1 * pow(1000, number_2.count('.000'))
				number_2 = float(number_2.replace('.', ''))
				numbers = [number_1, number_2]

		if len(numbers) == 1:
			for char in replace_str.keys():
				if char in raw_text:
					if char == 'tới':
						return [0, float(numbers[0])]
					elif char == 'từ':
						return [float(numbers[0]), float('inf')]
					elif char == 'trên':
						return [float(numbers[0]) + 1.0, float('inf')]
					elif char == 'dưới':
						return [0, float(numbers[0]) - 1.0]
			return [float(numbers[0])]
		else:
			return numbers

	def get_salary(self, MIN, MAX, num_records=None):
		"""

		:param MIN: Lương thấp nhất
		:param MAX: Lương cao nhất
		:param num_records: số lượng bản ghi muốn lấy
		:return: valid_records: list các bản ghi thỏa mãn
		"""
		df = pd.read_json(self.data)
		salary_list = df['salary']
		valid_records = []
		for i, salary_str in enumerate(salary_list):
			salary = self.convert(salary_str, heuristic=heuristic)
			for _ in salary:
				if MIN < _ < MAX:
					valid_records.append(df.iloc[[i]])
					break
			if num_records is not None and len(valid_records) > num_records:
				break
		return valid_records

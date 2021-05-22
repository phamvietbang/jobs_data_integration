import pandas as pd
import re

texts = ['Dưới 1 năm', '1 năm', '2 năm', 'Không yêu cầu', '8 - 10 năm', '1 - 2 năm kinh nghiệm', '4 - 0 năm']
heuristic = {

}
replace_str = {
	'trên': '>',
	'dưới': '<',
}


class Experience_management(object):
	def __init__(self, data_path):
		self.data = data_path

	def convert(self, text: str, heuristic: dict):
		text = text.lower()
		raw_text = text
		for char in replace_str.keys():
			text = text.replace(char, replace_str[char])
		numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
		if len(numbers) == 1:
			for char in replace_str.keys():
				if char in raw_text:
					if char == 'trên':
						return [float(numbers[0]) + 0.1, float('inf')]
					elif char == 'dưới':
						return [0, float(numbers[0]) - 0.1]
			return [float(numbers[0])]
		if len(numbers) > 0:
			numbers = [float(_) for _ in numbers]
			if numbers[0] > numbers[1]:
				return [float(numbers[0]) + 0.1, float('inf')]
			return numbers
		return numbers

	def get_experience(self, MIN, MAX, num_records=None):
		"""

		:param MIN: Lương thấp nhất
		:param MAX: Lương cao nhất
		:param num_records: số lượng bản ghi muốn lấy
		:return: valid_records: list các bản ghi thỏa mãn
		"""
		df = self.data
		salary_list = df['experience']
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

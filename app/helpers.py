from openpyxl import load_workbook

def get_data(form_data):
	print("========== starting get_data ==============")
	wb1 = load_workbook('/home/jberusch/GCYC/app/resources/eoy_dashboard.xlsx')
	wb2 = load_workbook('/home/jberusch/GCYC/app/resources/progress_to_date_edit.xlsx')
	prog = wb2['Sheet1']

	id = int(form_data['student_id'])

	for row in prog.rows:
		if (row[0].value == id):
			print(row)

	print("=========== ending get_data ===============")
	return "sample get_data output"
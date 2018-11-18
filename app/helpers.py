from openpyxl import load_workbook

# defining global vars
wb1 = load_workbook('/home/jberusch/GCYC/app/resources/eoy_dashboard.xlsx')
wb2 = load_workbook('/home/jberusch/GCYC/app/resources/progress_to_date_edit.xlsx')
prog = wb2['Sheet1']

# get all column headers
def get_col_headers():
	column_headers = []
	for cell in prog[1]:
		column_headers.append(cell.value)

	return column_headers

# find row corresponding to student id input 
def get_row(id):
	for row in prog.rows:
		if (row[0].value == id):
			return row

# print a row with labels
def print_row(headers,row):
	for i in range(len(headers)):
		print(headers[i])
		print(row[i].value)

def get_data(form_data):
	print("========== starting get_data ==============")

	# NOTE: probably want to expand so users can input multiple IDs
	id = int(form_data['student_id'])

	col_headers = get_col_headers()
	print(col_headers) # check

	student_row = get_row(id)
	print_row(col_headers,student_row)

	print("=========== ending get_data ===============")
	return "sample get_data output"
from openpyxl import load_workbook

# base_filepath = '/home/jberusch/GCYC/app/resources/' # use if CSIL
base_filepath = '/home/jberusch/Desktop/GCYC/app/resources/' # use if laptop

wb1 = load_workbook(base_filepath + 'eoy_dashboard.xlsx')
wb2 = load_workbook(base_filepath + 'progress_to_date_edit.xlsx')
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

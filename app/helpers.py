# library imports
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64

# helper imports
from parsing_xlsx import get_col_headers, get_row, print_row

def get_filter_data(form_data, student_row, col_headers):
	results = {}

	# for every filter, get the value if it's true
	if form_data['gender']:
		results['Gender'] = student_row[col_headers.index('Gender')].value
	if form_data['ms']:
		results['Middle School'] = student_row[col_headers.index('Middle School')].value
	if form_data['school']:
		results['School'] = student_row[col_headers.index('School')].value
	if form_data['advisor']:
		results['Advisor'] = student_row[col_headers.index('Advisor')].value

	return results

# PURPOSE: determine whether a string is a date
# really just tests if the 1st char is a number
def is_date(str):
	try:
		int(str[0])
		return True
	except ValueError:
		return False

# PURPOSE: get any data that has many points in time --> return ordered dict
# field: 'GPA', 'F Count', etc.
# to_ignore: columns in that field we don't want
def get_longitudinal_data(student_row, col_headers, field, to_ignore):
	res = collections.OrderedDict() # ordered dictionary to hold all results

	index = col_headers.index(field)
	i = 0
	current_header = col_headers[index]
	hit_date = False
	# loop until we hit something that isn't a date (get original field & EOY value)
	while True:
		print("start loop w/ current_header = " + current_header)
		# update bool once we've hit a date column
		if is_date(current_header):
			hit_date = True
		# if it's not a date & we've hit a date already, break
		elif hit_date:
			break
		
		# add item to dict if it's not in to_ignore
		if len(filter(lambda x: x == current_header, to_ignore)) == 0:
			print("adding " + current_header)
			res[current_header] = student_row[index-i].value
		
		i += 1
		current_header = col_headers[index-i]
		print("current_header: " + current_header)

	res = collections.OrderedDict(reversed(list(res.items())))
	return res

# plot all the GPAs for an individual student
def plot_longitudinal_data(values_dict):
	x_values = values_dict.keys()
	y_values = values_dict.values()

	figure, tmp = plt.subplots(nrows=1, ncols=1)
	# make figure bigger
	figure.set_size_inches(25,15)
	tmp.plot(x_values, y_values)

	fig_file = BytesIO()
	plt.savefig(fig_file, format='png')
	fig_file.seek(0)
	fig_data_png = base64.b64encode(fig_file.getvalue())
	return fig_data_png

	# figure.savefig('./app/static/plot.png') 
	# plt.close(figure)
	return

def get_individual_student_data(form_data):
	print("========== starting get_data ==============")

	# NOTE: probably want to expand so users can input multiple IDs
	id = int(form_data['student_id'])

	col_headers = get_col_headers()
	# print(col_headers) # check

	student_row = get_row(id)
	# check that a match was found
	if not student_row:
		return "Sorry, we couldn't find data on that student ID."

	print('===========================================')
	# print_row(col_headers,student_row)

	# get data asked for by filters
	filter_data = get_filter_data(form_data, student_row, col_headers)

	# always get GPA (users say they look @ that usually in chief)
	# get GPA last --> translates to "1st" in dictionary
	filter_data['GPA Dict'] = get_longitudinal_data(student_row, col_headers, 'GPA', ['Difference'])
	
	# DEBUG
	plot = plot_longitudinal_data(filter_data['GPA Dict'])

	res = {}
	res['data'] = filter_data
	res['plot'] = plot

	# TODO: show whether a student is on track!

	print("=========== ending get_data ===============")
	return res
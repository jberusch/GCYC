# library imports
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64

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

# PURPOSE: get the index of a field in the columns
# catch any error
def get_col_index(col_headers,field):
	try:
		index = col_headers.index(field)
		return index
	except ValueError:
		print("Column header not found")
		return -1

# PURPOSE: get any data that has many points in time --> return ordered dict
# field: 'GPA', 'F Count', etc.
# to_ignore: columns in that field we don't want
def get_longitudinal_data(student_row, col_headers, field, to_ignore):
	res = collections.OrderedDict() # ordered dictionary to hold all results

	index = get_col_index(col_headers,field)
	if index == -1: return res	
	i = 0
	current_header = col_headers[index]
	hit_date = False
	# loop until we hit something that isn't a date (get original field & EOY value)
	while True:
		# update bool once we've hit a date column
		if is_date(current_header):
			hit_date = True
		# if it's not a date & we've hit a date already, break
		elif hit_date:
			break
		
		# add item to dict if it's not in to_ignore
		if len(filter(lambda x: x == current_header, to_ignore)) == 0:
			res[current_header] = student_row[index-i].value
		
		i += 1
		current_header = col_headers[index-i]

	res = collections.OrderedDict(reversed(list(res.items())))
	return res

# plot all the GPAs for an individual student
def plot_longitudinal_data(values_dict):
	x_values = values_dict.keys()
	y_values = values_dict.values()

	print("x_values: ")
	print(x_values)
	print("y_values: ")
	print(y_values)

	# figure, ax = plt.subplots(nrows=1, ncols=1)
	# figure.set_size_inches(25,15) # make figure bigger
	# ax.plot(x_values, y_values)
	# ax.set_ylim(ymin=0) # start y axis at 0
	# ax.title('Students GPA')

	plt.plot(x_values,y_values)
	plt.title('Student\'s GPA')
	plt.xlabel('Data Measured')
	plt.ylabel('GPA')
	plt.ylim(ymin=0)
	plt.tight_layout()
	plt.tick_params(labelsize=20, labelrotation=90)

	figure = plt.gcf()
	figure.set_size_inches(25,15)

	# converting file to encoded png for rendering
	fig_file = BytesIO()
	plt.savefig(fig_file, format='png')
	fig_file.seek(0)
	fig_data_png = base64.b64encode(fig_file.getvalue())
	return fig_data_png

	# figure.savefig('./app/static/plot.png') 
	# plt.close(figure)
	return

def individual_on_track(student_row, col_headers):
	# get most recent F Count & GPA
	fc_i = get_col_index(col_headers,'F Count')
	gpa_i = get_col_index(col_headers,'GPA')
	f_count = fc_i == -1 if 0 else student_row[fc_i].value
	gpa = gpa_i == -1 if 0 else student_row[gpa_i].value

	# QUESTION: gpa >= 3.0 or > 3.0?
	return (f_count < 2 and gpa >= 3.0)	
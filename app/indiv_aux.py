# library imports
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64

# PURPOSE: grab all demographic info (Gender, MS, Advisory, etc.) from student row
def get_demographic_data(student_row,col_headers):
	res = collections.OrderedDict() # ordered just so it's not in super weird order
	# Start after ID & go until ECS Class (doesn't look helpful)
	current_header = col_headers[1]
	i = 1
	while current_header != 'ECS Class':
		res[current_header] = student_row[i].value
		i += 1
		current_header = col_headers[i]
	return res

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
def get_longitudinal_data(student_row, col_headers, field, to_ignore=[]):
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
		if not filter(lambda x: x == current_header, to_ignore):
			res[current_header] = student_row[index-i].value
		
		i += 1
		current_header = col_headers[index-i]

	res = collections.OrderedDict(reversed(list(res.items())))
	return res

# plot all the GPAs for an individual student
def plot_longitudinal_data(values_dict,field):
	x_values = values_dict.keys()
	y_values = values_dict.values()

	# set any #N/A values to None
	for i in range(len(y_values)):
		if not isinstance(y_values[i],(float,int,long)):
			y_values[i] = None

	plt.plot(x_values,y_values)
	plt.title('Student\'s '+field,fontsize=40)
	plt.xlabel('Date Measured',fontsize=30)
	plt.ylabel(field,fontsize=30)

	# ymin == 0 better for graphs of percentages
	if field == 'School Attendance':
		plt.ylim(ymin=0,ymax=1.05) # set ymin to 0
	elif field == 'Detentions':
		plt.ylim(ymin=0)
	# % LaSalle free never < 90%
	elif field == 'Percentage LaSalle Free':
		plt.ylim(ymin=0.9,ymax=1.005) # show trends meaningfully
	
	plt.tight_layout()
	plt.tick_params(labelsize=20, labelrotation=90)

	fig = plt.gcf()
	fig.set_size_inches(25,15)

	# converting file to encoded png for rendering
	fig_file = BytesIO()
	plt.savefig(fig_file, format='png')
	fig_file.seek(0)
	fig_data_png = base64.b64encode(fig_file.getvalue())
	fig.clear()
	return fig_data_png

def individual_on_track(student_row, col_headers):
	# get most recent F Count & GPA
	fc_i = get_col_index(col_headers,'F Count')
	gpa_i = get_col_index(col_headers,'GPA')
	f_count = fc_i == -1 if 0 else student_row[fc_i].value
	gpa = gpa_i == -1 if 0 else student_row[gpa_i].value

	print("f_count")
	print(f_count)
	print("gpa")
	print(gpa)

	# empty values in gpa or f_count
	if isinstance(f_count,str) or isinstance(gpa,str):
		return False

	return (f_count < 2 and gpa >= 3.0)	
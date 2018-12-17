# library imports
import collections

# helper imports
from app.parsing_xlsx import get_col_headers, get_row, print_row, get_rows_in_group
from app.indiv_aux import get_longitudinal_data, plot_longitudinal_data, individual_on_track, get_demographic_data
from app.group_aux import get_group_longitudinal_data, calc_percent_on_track, get_ids_in_group, build_basic_data

# global var for accessing metrics
metric_accessor = {
	'gpa': ['GPA', 'Difference'],
	'fc': ['F Count'],
	'ls': ['LaSalle Free'],
	'at': ['School Attendance','Difference2'],
	'dt': ['Detentions']
}

# TODO: tie this in with individual_student_data somehow
def get_plot_file(student_id,metric):
	col_headers = get_col_headers()
	student_row = get_row(int(student_id),col_headers)

	# throw err here if student_row not found
	if not student_row:
		print("get_plot_file: error finding student row")
		# TODOs

	arr = metric_accessor[metric]
	print(arr)
	metric_dict = get_longitudinal_data(student_row,col_headers,arr[0],arr[1:])
	plot_file = plot_longitudinal_data(metric_dict,arr[0])
	return plot_file

def get_individual_student_data(form_data):
	print("========== starting get_data ==============")

	# test for empty input
	if not form_data['student_id']:
		return "To get data on an individual student, we need their student ID #"

	# NOTE: probably want to expand so users can input multiple IDs
	student_id = int(form_data['student_id'])

	col_headers = get_col_headers()
	student_row = get_row(student_id,col_headers)
	# check that a match was found
	if not student_row:
		return "Sorry, we couldn't find data on that student ID."

	res = {}
	# get demographic data
	demo_data = get_demographic_data(student_row,col_headers)

	# always get GPA (users say they look @ that usually in chief)
	# get GPA last --> translates to "1st" in dictionary
	gpa_dict = get_longitudinal_data(student_row,col_headers,'GPA',['Difference'])
	fc_dict = get_longitudinal_data(student_row,col_headers,'F Count')
	ls_dict = get_longitudinal_data(student_row,col_headers,'LaSalle Free')
	at_dict = get_longitudinal_data(student_row,col_headers,'School Attendance',['Difference2'])
	dt_dict = get_longitudinal_data(student_row,col_headers,'Detentions')

	dicts = collections.OrderedDict()
	dicts['gpa'] = gpa_dict
	dicts['fc'] = fc_dict
	dicts['ls'] = ls_dict
	dicts['at'] = at_dict
	dicts['dt'] = dt_dict

	plots = collections.OrderedDict()
	# plot GPAs over time
	plots['gpa'] = plot_longitudinal_data(gpa_dict,'GPA')
	plots['fc'] = plot_longitudinal_data(fc_dict,'F Count')
	plots['ls'] = plot_longitudinal_data(ls_dict,'Percentage LaSalle Free')
	plots['at'] = plot_longitudinal_data(at_dict,'School Attendance')
	plots['dt'] = plot_longitudinal_data(dt_dict,'Detentions')

	metrics = collections.OrderedDict()
	metrics['gpa'] = 'GPA'
	metrics['fc'] = 'F Count'
	metrics['ls'] = 'LaSalles'
	metrics['at'] = 'School Attendance'
	metrics['dt'] = 'Detentions'

	res = {}
	res['demo_data'] = demo_data
	res['dicts'] = dicts
	res['plots'] = plots
	res['on_track'] = individual_on_track(student_row, col_headers)
	res['metrics'] = metrics

	print("=========== ending get_data ===============")
	return res

def get_group_data(form_data):
	print("get_group_data")
	res = {}

	col_headers = get_col_headers()

	# TODO: expand ms & gcyc_mem to display false options too
	adv,ms,gcyc_mem = form_data['adv_search'],form_data['ms'],form_data['gcyc_mem']

	if (adv and ms) or (ms and gcyc_mem) or (adv and gcyc_mem):
		return "Sorry, this tool only supports filtering groups by 1 criterion (advisor, Middle School, GCYC Member) right now!"
	elif adv:
		group_rows = get_rows_in_group(col_headers, 'Advisor', adv)
		filt = "Students From " + adv + "\'s Advisory"
	elif ms:
		group_rows = get_rows_in_group(col_headers, 'Middle School', 'GCMS')
		filt = "Only Former GCMS Attendees"
	elif gcyc_mem:
		group_rows = get_rows_in_group(col_headers, 'GCYC Member?', 'Yes')
		filt = "Only GCYC Members"
	else:
		return "You have to choose an option! Enter an advisor, check Middle School to see only GCMS students, or check GCYC Members to see only those studens."

	# might do stuff w/ all these matrices eventually
	gpa_matrix = get_group_longitudinal_data(group_rows,col_headers,'GPA',['Difference'])
	f_count_matrix = get_group_longitudinal_data(group_rows,col_headers,'F Count')
	ls_matrix = get_group_longitudinal_data(group_rows,col_headers,'LaSalle Free')
	att_matrix = get_group_longitudinal_data(group_rows,col_headers,'School Attendance',['Difference'])
	dt_matrix = get_group_longitudinal_data(group_rows,col_headers,'Detentions')

	percent_on_track = calc_percent_on_track(group_rows,col_headers)
	print("percent_on_track: " + str(percent_on_track) + "%")

	# Array of students: id, on_track?
	basic_data = build_basic_data(group_rows,col_headers)

	# add stuff to return dict
	res['basic_data'] = basic_data
	res['group_search_filter'] = filt
	res['percent_on_track'] = percent_on_track
	return res
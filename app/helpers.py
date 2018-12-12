# librayr imports
import collections

# helper imports
from parsing_xlsx import get_col_headers, get_row, print_row, get_rows_in_group
from indiv_aux import get_longitudinal_data, plot_longitudinal_data, individual_on_track, get_demographic_data
from group_aux import get_group_longitudinal_data, calc_percent_on_track, get_ids_in_group, build_basic_data

def get_individual_student_data(form_data):
	print("========== starting get_data ==============")

	# test for empty input
	if not form_data['student_id']:
		return "To get data on an individual student, we need their student ID #"

	# NOTE: probably want to expand so users can input multiple IDs
	id = int(form_data['student_id'])

	col_headers = get_col_headers()
	student_row = get_row(id)
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

	# TODO: create separate files for individual & group helper functions

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
# helper imports
from parsing_xlsx import get_col_headers, get_row, print_row, get_rows_in_group
from indiv_aux import get_filter_data, get_longitudinal_data, plot_longitudinal_data, individual_on_track
from group_aux import get_group_longitudinal_data, calc_percent_on_track

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

	# get data asked for by filters
	filter_data = get_filter_data(form_data, student_row, col_headers)

	# always get GPA (users say they look @ that usually in chief)
	# get GPA last --> translates to "1st" in dictionary
	filter_data['GPA Dict'] = get_longitudinal_data(student_row, col_headers, 'GPA', ['Difference'])

	# plot GPAs over time
	# TODO: remove empty fields from plot
	plot = plot_longitudinal_data(filter_data['GPA Dict'])

	res = {}
	res['data'] = filter_data
	res['plot'] = plot
	res['on_track'] = individual_on_track(student_row, col_headers)

	print("=========== ending get_data ===============")
	return res

	# TODO: create separate files for individual & group helper functions

def get_group_data(form_data):
	print("get_group_data")
	res = {}

	col_headers = get_col_headers()

	# TODO: expand ms & gcyc_mem to display false options too
	# TODO: handle multiple inputs
	adv,ms,gcyc_mem = form_data['adv_search'],form_data['ms'],form_data['gcyc_mem']

	if (adv and ms) or (ms and gcyc_mem) or (adv and gcyc_mem):
		return "Sorry, this tool only supports filtering groups by 1 criterion (advisor, Middle School, GCYC Member) right now!"
	elif adv:
		group_rows = get_rows_in_group(col_headers, 'Advisor', adv)
	elif ms:
		group_rows = get_rows_in_group(col_headers, 'Middle School', 'GCMS')
	elif gcyc_mem:
		group_rows = get_rows_in_group(col_headers, 'GCYC Member?', 'Yes')
	else:
		return "You have to choose an option! Enter an advisor, check Middle School to see only GCMS students, or check GCYC Members to see only those studens."

	gpa_matrix = get_group_longitudinal_data(group_rows,col_headers,'GPA',['Difference'])
	f_count_matrix = get_group_longitudinal_data(group_rows,col_headers,'F Count')
	ls_matrix = get_group_longitudinal_data(group_rows,col_headers,'LaSalle Free')
	att_matrix = get_group_longitudinal_data(group_rows,col_headers,'School Attendance',['Difference'])
	dt_matrix = get_group_longitudinal_data(group_rows,col_headers,'Detentions')

	percent_on_track = calc_percent_on_track(group_rows,col_headers)
	print("percent_on_track: " + str(percent_on_track) + "%")

	return res
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import IndividualSearchForm, GroupSearchForm
import app.helpers as helpers

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title = 'Home')

@app.route('/search', methods=['GET','POST'])
def search():
	individual_form = IndividualSearchForm()
	group_form = GroupSearchForm()

	# searching by individual student
	if individual_form.validate_on_submit() and individual_form.indiv_submit.data:
		print("individual form!")
		form = individual_form
		form_data = {
			"student_id": form.student_id.data,
			"gender": form.gender.data,
			"ms": form.ms.data,
			"school": form.school.data,
			"advisor": form.advisor.data
		}
		res = helpers.get_individual_student_data(form_data)

		# if get_individual_student_data returns a string, there was an error --> display the error message
		if isinstance(res,str):
			print(res)
			return render_template('search.html',title='Search',individual_form=individual_form,
				group_form=group_form,error_msg=res)

		return render_template('search.html', title='Search', individual_form=individual_form, 
			group_form=group_form, raw_data=res['data'], plot=res['plot'], on_track=res['on_track'])
	
	# searching by group
	if group_form.validate_on_submit() and group_form.group_submit.data:
		print("group form!")
		form = group_form
		form_data = {
			"adv_search": form.adv_search.data,
			"ms": form.ms.data,
			"gcyc_mem": form.gcyc_mem.data
		}
		print(form_data)
		res = helpers.get_group_data(form_data)

		# if get_group_data returns a string, there was an error --> display the error message
		if isinstance(res,str):
			return render_template('search.html',title='Search',individual_form=individual_form,
				group_form=group_form,error_msg=res)

		return render_template('search.html', title='Search', individual_form=individual_form,
			group_form=group_form)

	return render_template('search.html', title='Search', individual_form=individual_form, group_form=group_form)

@app.route('/search_results', methods=['GET','POST'])
def search_results():
	return "search results go here"
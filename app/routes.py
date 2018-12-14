# library imports
import os
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename

# local imports
from app import app
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

		print(res['plots']['gpa'])

		return render_template('search.html', title='Search', individual_form=individual_form, group_form=group_form, 
			demo_data=res['demo_data'], on_track=res['on_track'], dicts=res['dicts'], plots=res['plots'], metrics=res['metrics'])
	
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
			group_form=group_form, basic_data=res['basic_data'], group_search_filter=res['group_search_filter'],
			percent_on_track=res['percent_on_track'])

	return render_template('search.html', title='Search', individual_form=individual_form, group_form=group_form)


# TODO: Figure out this file upload stuff!
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['xlsx','xls','csv']) # TODO: add extension

@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		# make sure a file has been uploaded
		if 'file' not in request.files:
			flash('Sorry, you didn\'t choose a file!')
			return redirect(request.url) # go back from page you requested from (probably same page)

		fp = request.files['file']
		if not fp or fp.filename == '':
			flash('Sorry, you didn\'t choose a file!')
			return redirect(request.url)

		filename = secure_filename(fp.filename)
		# make sure filetype is allowed
		if not allowed_file(filename):
			flash('Sorry, we can only accept Excel or CSV files!')
			return redirect(request.url)

		fp.save(os.path.join(app.root_path, 'resources/' + filename)) # app root in resources subdirectory
		flash("File uploaded successfully!")

	return render_template('upload.html',title='Upload')

@app.route('/manual')
def manual():
	return render_template('manual.html',title='Manual')
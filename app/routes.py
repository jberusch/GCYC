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

		print("==================== returning ===================")
		print(res['metrics'])
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
			group_form=group_form, basic_data=res['basic_data'], group_search_filter=res['group_search_filter'])

	return render_template('search.html', title='Search', individual_form=individual_form, group_form=group_form)


# TODO: Figure out this file upload stuff!
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['.xlsx']) # TODO: add extension

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html',title='Upload')

@app.route('/manual')
def manual():
	return "GARY's manual will go here"
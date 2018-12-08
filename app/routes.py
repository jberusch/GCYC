from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import SearchForm
import app.helpers as helpers

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title = 'Home')

@app.route('/search', methods=['GET','POST'])
def search():
	form = SearchForm()
	if form.validate_on_submit():
		form_data = {
			"select_individual": form.select_individual.data,
			"select_group": form.select_group.data,
			"student_id": form.student_id.data,
			"gender": form.gender.data,
			"ms": form.ms.data,
			"school": form.school.data,
			"advisor": form.advisor.data
		}
		res = helpers.get_individual_student_data(form_data)
		return render_template('search.html', title = 'Search', form = form, raw_data = res['data'], plot = res['plot'])

	return render_template('search.html', title = 'Search', form = form)

@app.route('/search_results', methods=['GET','POST'])
def search_results():
	return "search results go here"
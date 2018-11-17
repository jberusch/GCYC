from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import SearchForm


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title = 'Home')

@app.route('/search', methods=['GET','POST'])
def search():
	form = SearchForm()
	if form.validate_on_submit():
		form_data = {
			"student_id": form.student_id.data,
			"filter1": form.filter1.data
		}
		return render_template('search.html', title = 'Search', form = form, results = form_data)

	return render_template('search.html', title = 'Search', form = form)

@app.route('/search_results', methods=['GET','POST'])
def search_results():
	return "search results go here"
from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SearchForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title = 'Home')

@app.route('/search', methods=['GET','POST'])
def search():
	form = SearchForm()
	if form.validate_on_submit():
		flash('Student ID: {}, filter1: {}'.format(form.student_id.data, form.filter1.data))
		return redirect(url_for('search_results'))

	return render_template('search.html', title = 'Search', form = form)

@app.route('/search_results')
def search_results():
	return "search results go here"
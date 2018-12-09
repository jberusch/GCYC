from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField

class IndividualSearchForm(FlaskForm):
	student_id = StringField('Student ID #')
	gender = BooleanField('Gender')
	ms = BooleanField('Middle School')
	school = BooleanField('School')
	advisor = BooleanField('Advisor')
	indiv_submit = SubmitField('Get Data')

class GroupSearchForm(FlaskForm):
	# adv_bool = BooleanField('Advisory')
	adv_search = StringField('Advisor')
	ms = BooleanField('Middle School')
	gcyc_mem = BooleanField('GCYC Members')
	group_submit = SubmitField('Get Data')
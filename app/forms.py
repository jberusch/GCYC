from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# help with 

class SearchForm(FlaskForm):
	student_id = StringField('Student ID #', validators=[DataRequired()])
	gender = BooleanField('Gender')
	ms = BooleanField('Middle School')
	school = BooleanField('School')
	advisor = BooleanField('Advisor')
	submit = SubmitField('Get Data')
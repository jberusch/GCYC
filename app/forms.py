from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
	student_id = StringField('Student ID #', validators=[DataRequired()])
	filter1 = BooleanField('Filter 1')
	submit = SubmitField('Get Data')
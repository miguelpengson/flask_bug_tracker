from flask import request_started
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length


class TrackerForm(FlaskForm):
    # Each field is given a label as a first argument
    project = StringField('Project', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('high', 'High'), ('moderate', 'Moderate'), ('low', 'Low')])
    progress = SelectField('Progress', choices=[('completed', 'Completed'), 
                            ('in-progress', 'In Progress'), ('not-started', 'Not Started')])
    submit = SubmitField('Submit')
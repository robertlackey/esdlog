from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, InputRequired
from wtforms.widgets import TextArea

class SubmitForm(FlaskForm):
    company = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    position = StringField('Position', validators=[DataRequired(), Length(max=100)])
    type = SelectField(
        'Type', 
        choices=[('Application/Resume', 'Application/Resume'),
                 ('Query', 'Query'),
                 ('Interview', ('Interview'))], 
        validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    method = SelectField(
        'Method', 
        choices=[('Online', 'Online'), 
                 ('In-Person', 'In-Person'),
                 ('Phone', 'Phone'),
                 ('Email', 'Email')], 
        validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired(), Length(max=100)])
    notes = StringField('Notes', validators=[Length(max=1000)],  widget=TextArea())

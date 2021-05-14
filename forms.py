from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired,Length

class registerForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=30)])
    amt = IntegerField('Amount')
    submit = SubmitField('Submit')
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    name = StringField('Ad', validators=[Required()])
    room = StringField('Oda', validators=[Required()])
    submit = SubmitField('Odaya gir')

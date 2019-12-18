from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    """Kullanıcı adı ve oda bilgileri ile giriş yap."""
    name = StringField('Ad', validators=[Required()])
    room = StringField('Oda', validators=[Required()])
    submit = SubmitField('Odaya gir')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email:',
                        validators=[DataRequired(), Length(min=6, max=120)],
                        render_kw={
                            'type': 'email',
                            'class': 'form-control mb-4',
                            'placeholder': 'E-mail'
                        })
    pwd = PasswordField('Password:',
                        validators=[DataRequired(), Length(min=6, max=120)],
                        render_kw={
                            'type': 'password',
                            'class': 'form-control mb-4',
                            'placeholder': 'Password'
                        })
    remember_me = BooleanField('Remember Me',
                               render_kw={
                                   'type': 'checkbox',
                                   'class': 'custom-control-input',
                               })
    submit = SubmitField('Login In',
                         render_kw={
                             'type': 'submit',
                             'class': 'btn btn-info btn-block my-4',
                         })

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)
        if not user:
            raise ValidationError("The Email doesn't exist.")

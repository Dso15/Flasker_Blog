from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.widgets import TextArea

from website.models import User



# -------------------- User Forms --------------------
class LoginForm(FlaskForm):
    email = StringField('Email/Username:')
    password = PasswordField('Password:')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30), EqualTo('re_password')])
    re_password = PasswordField('Confirm Password:', validators=[DataRequired()])
    submit = SubmitField('Register')

class EditAccountForm(FlaskForm):
    identifier = StringField()
    name = StringField('Name:', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')

class ConfirmEmailForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Confirm Email')

class ChangePasswordForm(FlaskForm):
    identifier = StringField()
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=30), EqualTo('re_password', message="'Password' must be equal to 'Confirm Password'.")])
    re_password = PasswordField('Confirm Password:', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class RequestResetPasswordForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
# -------------------- End of User Forms --------------------


# -------------------- Post Forms --------------------
class AddPostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    # content = StringField('Content:', validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content:', validators=[DataRequired()])
    slug = StringField('Slug:', validators=[DataRequired()])
    submit = SubmitField('Add Post')



class SearchForm(FlaskForm):
    searched = StringField('Searched:', validators=[DataRequired()])
    submit = SubmitField('Search')
# -------------------- End of Post Forms --------------------
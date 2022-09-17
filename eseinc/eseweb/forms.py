from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, EmailField, PasswordField, StringField, IntegerField, SelectField, TextAreaField
from flask_wtf.file import FileField as FileIn
from wtforms.validators import DataRequired, Email, Length, EqualTo

class MakePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=150)])
    post_preview = StringField('preview', validators=[DataRequired()])
    post_body = TextAreaField()
    category = SelectField('Category', coerce=int)
    mins_read = IntegerField()
    photo = FileIn(validators=[DataRequired()])
    submit = SubmitField('Post')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=150)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=50, max=9000)])
    post_preview = StringField('preview', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    mins_read = IntegerField()
    submit = SubmitField('Post')



class CreateProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=200)])
    project_description = StringField('Project description', validators=[DataRequired(), Length(min=2, max=600)])
    client_name = StringField('Client name (detail)', validators=[DataRequired(), Length(min=2, max=200)])
    client_review = StringField('Client Review or thoughts', validators=[DataRequired(), Length(min=2, max=300)])
    submit = SubmitField('Create Project')




class SearchForm(FlaskForm):
    search = StringField('Search text', validators=[DataRequired(), Length(min=2, max=50)])
    search_by = SelectField('Search by', validators=[DataRequired()], choices=[('title', 'Post title'), ('body', 'Post body'), ('all', 'all')])
    submit = SubmitField('Search')





class AddReviewForm(FlaskForm):
    client_name = StringField('Client name (detail)', validators=[DataRequired(), Length(min=2, max=200)])
    client_review = StringField('Client Review or thoughts', validators=[DataRequired(), Length(min=2, max=300)])
    submit = SubmitField('Add Review')


class AddEmailForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired(), Email(), Length(min=2, max=150)])
    submit = SubmitField('Add Email')

class RegisterForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired(), Email(), Length(min=2, max=150)])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Your Email', validators=[DataRequired(), Email(), Length(min=2, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateCategoryForm(FlaskForm):
    category_name = StringField('Category name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Category')

class TestUploadForm(FlaskForm):
    photo = FileIn(validators=[DataRequired()])
    submit = SubmitField('Upload File')


class AddFAQ(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(min=2, max=700)])
    answer = StringField('Answer', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Add FAQ')
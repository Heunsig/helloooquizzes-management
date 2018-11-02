from flask_wtf import FlaskForm
from wtforms import StringField, TextField, BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create')


class NewGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create')


class NewQuizForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    example_1 = TextField('Example 1')
    example_2 = TextField('Example 2')
    example_3 = TextField('Example 3')
    example_4 = TextField('Example 4')
    correct_answer_1 = BooleanField('Example 1 is correct answer')
    correct_answer_2 = BooleanField('Example 2 is correct answer')
    correct_answer_3 = BooleanField('Example 3 is correct answer')
    correct_answer_4 = BooleanField('Example 4 is correct answer')
    time_limit = TextField('Time Limt(sec)', default=20, validators=[DataRequired()])
    submit = SubmitField('Create')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, TextAreaField, SelectMultipleField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email, Length, InputRequired


class AtLeast(object):
    def __init__(self, min=1, group=[], message=None):
        self.min = min
        self.group = group
        if not message:
            message = 'These fields must be required at least %i' % (min)
        self.message = message

    def __call__(self, form, field):
        tracker = []
        for item in self.group:
            if form[item].data:
                tracker.append(True)

        if len(tracker) < self.min:
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    submit = SubmitField('Login')


class NewQuizForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    submit = SubmitField('Submit')


class NewQuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(max=120)])
    choice_1 = StringField('Choice 1', validators=[Length(max=120), AtLeast(min=1, group=['choice_1', 'choice_2', 'choice_3', 'choice_4'])])
    choice_2 = StringField('Choice 2', validators=[Length(max=120)])
    choice_3 = StringField('Choice 3', validators=[Length(max=120)])
    choice_4 = StringField('Choice 4', validators=[Length(max=120)])
    correct_answer_1 = BooleanField('Choice 1 is correct answer', validators=[AtLeast(min=1, group=['correct_answer_1', 'correct_answer_2', 'correct_answer_3', 'correct_answer_4'])])
    correct_answer_2 = BooleanField('Choice 2 is correct answer')
    correct_answer_3 = BooleanField('Choice 3 is correct answer')
    correct_answer_4 = BooleanField('Choice 4 is correct answer')
    time_limit = StringField('Time Limt(sec)', default=20, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_time_limit(form, field):
        if int(field.data) > 1800:
            raise ValidationError('Time limt must be within 1800 sec')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(max=60)])
    submit = SubmitField('Submit')

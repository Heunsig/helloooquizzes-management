from app import app, db, bcrypt, login_manager
from flask import render_template, url_for, redirect, flash, request, jsonify
from app.forms import *
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
# from helpers import get_correct_answers


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/test')
def test_gmae():
    return 'Hi'


@app.route('/api/quiz/<int:quiz_id>/player', methods=['POST'])
def add_player(quiz_id):
    # print(request.json['data'])
    player = Player(quiz_id=quiz_id, name=request.json['name'], score=request.json['score'])
    db.session.add(player)
    db.session.commit()

    return jsonify(result='success')


@app.route('/api/quiz/list')
def quiz_list():
    quizzes = Quiz.query.filter_by(state='active').order_by(Quiz.created_at.desc())

    payload = []
    for quiz in quizzes:
        data = {
            'id': quiz.id,
            'name': quiz.name,
            'description': quiz.description,
            'creator': quiz.user.username,
            'created_at': quiz.created_at.strftime('%m/%d/%Y')
        }

        payload.append(data)

    return jsonify(result=payload)


@app.route('/api/quiz/<int:quiz_id>')
def play_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id).first()

    questions = []
    for question in quiz.questions:
        if question.state == 'active':
            choices = []
            for choice in question.choices:
                choice = {
                    'content': choice.content,
                    'order': choice.order
                }
                choices.append(choice)

            question = {
                'id': question.id,
                'question': question.question,
                'choices': choices,
                'correct_answer': question.correct_answer,
                'time_limit': question.time_limit
            }

            questions.append(question)

    payload = {
        'quiz': {
            'name': quiz.name,
            'creator': quiz.user.username,
            'quiz_id': quiz.id
        },
        'questions': questions
    }

    return jsonify(result=payload)


@app.route('/')
def home():
    return render_template('home.html')


# @app.route("/quiz")
# def quiz():
#     quizzes = Quiz.query.order_by(Quiz.created_at.desc())
#     return render_template('quiz.html', title='Quizzes', quizzes=quizzes)


@app.route("/my_quiz")
@login_required
def my_quiz():
    # page = request.args.get('page', 1, type=int)
    quizzes = Quiz.query.filter_by(user_id=current_user.id).order_by(Quiz.created_at.desc())
    return render_template('my_quiz.html', title='My Quizzes', quizzes=quizzes)


@app.route("/my_quiz/<int:quiz_id>")
@login_required
def my_quiz_detail(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template('my_quiz_detail.html',
                           title=quiz.name,
                           quiz=quiz)


@app.route('/quiz/<int:quiz_id>/create_question', methods=['GET', 'POST'])
@login_required
def new_question(quiz_id):
    form = NewQuestionForm()
    if form.validate_on_submit():
        correct_answer = ''
        if form.correct_answer_1.data:
            correct_answer += '1,'

        if form.correct_answer_2.data:
            correct_answer += '2,'

        if form.correct_answer_3.data:
            correct_answer += '3,'

        if form.correct_answer_4.data:
            correct_answer += '4,'

        correct_answer = correct_answer[:-1]

        question = Question(quiz_id=quiz_id,
                            question=form.question.data,
                            correct_answer=correct_answer,
                            time_limit=form.time_limit.data)

        if form.choice_1.data:
            question.choices.append(Choice(content=form.choice_1.data, order=1))
        if form.choice_2.data:
            question.choices.append(Choice(content=form.choice_2.data, order=2))
        if form.choice_3.data:
            question.choices.append(Choice(content=form.choice_3.data, order=3))
        if form.choice_4.data:
            question.choices.append(Choice(content=form.choice_4.data, order=4))

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('new_question', quiz_id=quiz_id, mode='create'))
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template('new_question.html', form=form, quiz=quiz, mode='create')


@app.route('/question/<int:question_id>/update', methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    form = NewQuestionForm()
    if form.validate_on_submit():
        question.question = form.question.data
        question.time_limit = form.time_limit.data

        correct_answer = ''
        if form.correct_answer_1.data:
            correct_answer += '1,'

        if form.correct_answer_2.data:
            correct_answer += '2,'

        if form.correct_answer_3.data:
            correct_answer += '3,'

        if form.correct_answer_4.data:
            correct_answer += '4,'

        correct_answer = correct_answer[:-1]

        question.correct_answer = correct_answer

        question = Question(quiz_id=question.quiz_id,
                            question=form.question.data,
                            correct_answer=correct_answer,
                            time_limit=form.time_limit.data)

        if form.choice_1.data:
            if Choice.query.filter_by(question_id=question_id, order=1).one_or_none():
                Choice.query.filter_by(question_id=question_id, order=1).one_or_none().content = form.choice_1.data
            else:
                db.session.add(Choice(question_id=question_id, content=form.choice_1.data, order=1))
        else:
            if Choice.query.filter_by(question_id=question_id, order=1).one_or_none():
                db.session.delete(Choice.query.filter_by(question_id=question_id, order=1).first())

        if form.choice_2.data:
            if Choice.query.filter_by(question_id=question_id, order=2).one_or_none():
                Choice.query.filter_by(question_id=question_id, order=2).one_or_none().content = form.choice_2.data
            else:
                db.session.add(Choice(question_id=question_id, content=form.choice_2.data, order=2))
        else:
            if Choice.query.filter_by(question_id=question_id, order=2).one_or_none():
                db.session.delete(Choice.query.filter_by(question_id=question_id, order=2).first())

        if form.choice_3.data:
            if Choice.query.filter_by(question_id=question_id, order=3).one_or_none():
                Choice.query.filter_by(question_id=question_id, order=3).one_or_none().content = form.choice_3.data
            else:
                db.session.add(Choice(question_id=question_id, content=form.choice_3.data, order=3))
        else:
            if Choice.query.filter_by(question_id=question_id, order=3).one_or_none():
                db.session.delete(Choice.query.filter_by(question_id=question_id, order=3).first())

        if form.choice_4.data:
            if Choice.query.filter_by(question_id=question_id, order=4).one_or_none():
                Choice.query.filter_by(question_id=question_id, order=4).one_or_none().content = form.choice_4.data
            else:
                db.session.add(Choice(question_id=question_id, content=form.choice_4.data, order=4))
        else:
            if Choice.query.filter_by(question_id=question_id, order=4).one_or_none():
                db.session.delete(Choice.query.filter_by(question_id=question_id, order=4).first())

        db.session.commit()
        flash('Your question has been updated!', 'success')
        return redirect(url_for('update_question', question_id=question_id, mode='edit'))

    elif request.method == 'GET':
        correct_answers = question.correct_answer.split(',')

        form.question.data = question.question
        form.time_limit.data = question.time_limit
        form.choice_1.data = Choice.query.filter_by(question_id=question.id, order=1).one_or_none().content if Choice.query.filter_by(question_id=question.id, order=1).one_or_none() else None
        form.choice_2.data = Choice.query.filter_by(question_id=question.id, order=2).one_or_none().content if Choice.query.filter_by(question_id=question.id, order=2).one_or_none() else None
        form.choice_3.data = Choice.query.filter_by(question_id=question.id, order=3).one_or_none().content if Choice.query.filter_by(question_id=question.id, order=3).one_or_none() else None
        form.choice_4.data = Choice.query.filter_by(question_id=question.id, order=4).one_or_none().content if Choice.query.filter_by(question_id=question.id, order=4).one_or_none() else None

        if '1' in correct_answers:
            form.correct_answer_1.data = True
        if '2' in correct_answers:
            form.correct_answer_2.data = True
        if '3' in correct_answers:
            form.correct_answer_3.data = True
        if '4' in correct_answers:
            form.correct_answer_4.data = True

    return render_template('new_question.html', form=form, quiz=question.quiz, mode='edit')


@app.route('/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.quiz.user != current_user:
        abort(403)
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return jsonify(result='success')


@app.route("/question/<int:question_id>/toggle", methods=['POST'])
@login_required
def toggle_question_activation(question_id):
    question = Question.query.get_or_404(question_id)
    if question.state == 'active':
        question.state = 'inactive'
    else:
        question.state = 'active'

    db.session.commit()
    return jsonify(result=question.state)


@app.route('/quiz/new', methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = NewQuizForm()
    if form.validate_on_submit():
        quiz = Quiz(name=form.name.data, description=form.description.data, user=current_user)
        db.session.add(quiz)
        db.session.commit()
        flash("You've successfully made new quiz.", 'success')
        return redirect(url_for('new_quiz', quiz_id=quiz.id))
    return render_template('new_quiz.html', form=form)


@app.route("/quiz/<int:quiz_id>/update", methods=['GET', 'POST'])
@login_required
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = NewQuizForm()
    if form.validate_on_submit():
        quiz.name = form.name.data
        quiz.description = form.description.data
        quiz.updated_at = datetime.now()
        db.session.commit()
        flash('Your quiz has been updated!', 'success')
        return redirect(url_for('update_quiz', quiz_id=quiz_id))
    elif request.method == 'GET':
        form.name.data = quiz.name
        form.description.data = quiz.description
    return render_template('new_quiz.html', form=form)


@app.route("/quiz/<int:quiz_id>/delete", methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user != current_user:
        abort(403)
    db.session.delete(quiz)
    db.session.commit()
    flash('Your quiz has been deleted!', 'success')
    return jsonify(result='success')


@app.route("/quiz/<int:quiz_id>/toggle", methods=['POST'])
@login_required
def toggle_activation(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.state == 'active':
        quiz.state = 'inactive'
    else:
        quiz.state = 'active'

    db.session.commit()
    return jsonify(result=quiz.state)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')


@app.route('/player_log/<int:quiz_id>')
def player_log(quiz_id):
    players = Player.query.filter_by(quiz_id=quiz_id).order_by(Player.created_at.desc())
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template('player_log.html', title='Player Log', quiz=quiz, players=players)


@app.route('/account')
def account():
    return render_template('account.html', title='Account')
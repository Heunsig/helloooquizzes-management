from app import app, db, bcrypt, login_manager
from flask import render_template, url_for, redirect, flash, request, jsonify
from app.forms import *
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/api/game/list')
def game_list():
    games = Game.query.all()

    payload = []
    for game in games:
        data = {
            'id': game.id,
            'name': game.name,
            'description': game.description,
            'creator': game.user.username,
            'created_at': game.created_at.strftime('%Y-%m-%d')
        }

        payload.append(data)

    return jsonify(result=payload)


@app.route('/api/game/<int:game_id>')
def play_game(game_id):
    game = Game.query.filter_by(id=game_id).first()

    questions = []
    for question in game.questions:
        choices = []
        for choice in question.choices:
            choice = {
                'content': choice.content,
                'order': choice.order
            }
            choices.append(choice)

        question = {
            'question': question.question,
            'choices': choices,
            'correct_answer': question.correct_answer,
            'time_limit': question.time_limit
        }

        questions.append(question)

    payload = {
        'game': {
            'name': game.name,
            'creator': game.user.username,
            'game_id': game.id
        },
        'questions': questions
    }

    return jsonify(result=payload)


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/game")
def game():
    games = Game.query.order_by(Game.created_at.desc())
    return render_template('game.html', title='My Games', games=games)


@app.route("/my_game")
@login_required
def my_game():
    # page = request.args.get('page', 1, type=int)
    games = Game.query.order_by(Game.created_at.desc())
    return render_template('my_game.html', title='My Games', games=games)


@app.route("/my_game/<int:game_id>")
@login_required
def my_game_detail(game_id):
    game = Game.query.filter_by(id=game_id).first()
    return render_template('my_game_detail.html', title=game.name, game=game)


@app.route('/game/<int:game_id>/create_question', methods=['GET', 'POST'])
@login_required
def new_question(game_id):
    form = NewQuizForm()
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

        question = Question(game_id=game_id,
                            question=form.question.data,
                            correct_answer=correct_answer,
                            time_limit=form.time_limit.data)

        if form.example_1.data:
            question.choices.append(Choice(content=form.example_1.data, order=1))
        if form.example_2.data:
            question.choices.append(Choice(content=form.example_2.data, order=2))
        if form.example_3.data:
            question.choices.append(Choice(content=form.example_3.data, order=3))
        if form.example_4.data:
            question.choices.append(Choice(content=form.example_4.data, order=4))

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('new_question', game_id=game_id))
    game = Game.query.filter_by(id=game_id).first()
    return render_template('new_question.html', form=form, game=game)


@app.route('/new_game', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGameForm()
    if form.validate_on_submit():
        game = Game(name=form.name.data, description=form.description.data, user=current_user)
        db.session.add(game)
        db.session.commit()
        flash("You've successfully made new game.", 'success')
        return redirect(url_for('new_question', game_id=game.id))
    return render_template('new_game.html', form=form)


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

from flask import Flask, render_template
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.cards import Cards
from data.owner_money_class import Owner_money
from data.resources import Resource
from data.type_operations import Type_of_operation
from data.users import User
from forms.card import CardForm
from forms.owner_money import Owner_moneyForm
from forms.type_operation import Type_OperationForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/family_bud.sqlite")
    app.run()


@app.route('/')
def index():
    return render_template('index.html', username='Andrey')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/cards',  methods=['GET', 'POST'])
@login_required
def add_cards():
    form = CardForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cards = Cards()
        cards.title = form.title.data
        cards.content = form.content.data
        current_user.cards.append(cards)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('cards.html', title='Добавление карты',
                           form=form)


@app.route('/type_operation',  methods=['GET', 'POST'])
@login_required
def add_type_operation():
    form = Type_OperationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        type_operations = Type_of_operation()
        type_operations.title = form.title.data
        type_operations.content = form.content.data
        if form.type_operation.data == 'Приход':
            type_operations.type_operation = 1
        elif form.type_operation.data == 'Приход':
            type_operations.type_operation = 2
        else:
            type_operations.type_operation = 3
        current_user.type_of_operation.append(type_operations)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('type_operation.html', title='Добавление типа операций',
                           form=form)


@app.route('/owner_money',  methods=['GET', 'POST'])
@login_required
def add_owner_money():
    form = Owner_moneyForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        owner = Owner_money()
        owner.title = form.title.data
        owner.content = form.content.data
        current_user.owner_money.append(owner)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('owner_money.html', title='Добавление owner',
                           form=form)


@app.route('/resource',  methods=['GET', 'POST'])
@login_required
def add_resource():
    form = Owner_moneyForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        resource = Resource()
        resource.title = form.title.data
        resource.content = form.content.data
        current_user.resource.append(resource)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('resource.html', title='Добавление owner',
                           form=form)


if __name__ == '__main__':
    main()
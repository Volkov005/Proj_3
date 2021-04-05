import datetime
import sqlite3

from flask import Flask, render_template, request
from flask_restful import abort
from sqlalchemy import create_engine, desc
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.cards import Cards
from data.operations import Operations
from data.owner_money_class import Owner_money
from data.resources import Resource
from data.sub_operations import Sub_operation
from data.type_operations import Type_of_operation
from data.users import User
from forms.card import CardForm
from forms.operation import OperationForm
from forms.owner_money import Owner_moneyForm
from forms.resource import ResourceForm
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
    return render_template('index1.html', username='Andrey')


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


@app.route('/cards', methods=['GET', 'POST'])
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
        return redirect('/cards_table')
    return render_template('cards.html', title='Добавление карты',
                           form=form, trigger="Добавление")


@app.route('/type_operation', methods=['GET', 'POST'])
@login_required
def add_type_operation():
    form = Type_OperationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        type_operations = Type_of_operation()
        type_operations.title = form.title.data
        type_operations.content = form.content.data
        type_operations.type_operation = form.type_operation.data
        current_user.type_of_operation.append(type_operations)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/type_operation_table')
    return render_template('type_operation.html', title='Добавление типа операций',
                           form=form)


@app.route('/owner_money', methods=['GET', 'POST'])
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
        return redirect('/owner_money_table')
    return render_template('owner_money.html', title='Добавление owner',
                           form=form)


@app.route('/resource', methods=['GET', 'POST'])
@login_required
def add_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        resource = Resource()
        resource.title = form.title.data
        resource.content = form.content.data
        current_user.resource.append(resource)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/resource_table')
    return render_template('resource.html', title='Добавление resource',
                           form=form)


@app.route('/cards_table')
def get_cards_table():
    db_sess = db_session.create_session()
    cards = db_sess.query(Cards).filter(Cards.user_id == current_user.id).order_by(Cards.created_date)
    sub_oper = db_sess.query(Sub_operation).filter(Sub_operation.user_id == current_user.id)
    return render_template("cards_table.html", cards=cards, sub_oper=sub_oper)


@app.route('/type_operation_table')
def get_type_operation_table():
    db_sess = db_session.create_session()
    type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.user_id == current_user.id)
    return render_template("type_operation_table.html", type_operation=type_operation)


@app.route('/owner_money_table')
def get_owner_money_table():
    db_sess = db_session.create_session()
    owner_money = db_sess.query(Owner_money).filter(Owner_money.user_id == current_user.id)
    return render_template("owner_money_table.html", owner_money=owner_money)


@app.route('/resource_table')
def get_resource_table():
    db_sess = db_session.create_session()
    resource = db_sess.query(Resource).filter(Resource.user_id == current_user.id)
    return render_template("resource_table.html", resource=resource)


@app.route('/cards/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cards(id):
    form = CardForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        cards = db_sess.query(Cards).filter(Cards.id == id,
                                            Cards.user == current_user
                                            ).first()
        if cards:
            form.title.data = cards.title
            form.content.data = cards.content
            form.balance.data = cards.balance
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cards = db_sess.query(Cards).filter(Cards.id == id,
                                            Cards.user == current_user
                                            ).first()
        if cards:
            cards.title = form.title.data
            cards.content = form.content.data
            cards.created_date = datetime.datetime.now()
            db_sess.commit()
            return redirect('/cards_table')
        else:
            abort(404)
    return render_template('cards.html',
                           title='Редактирование новости',
                           form=form,
                           trigger="Редактирование",
                           )


@app.route('/type_operation/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_type_operation(id):
    form = Type_OperationForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.id == id,
                                                                 Type_of_operation.user == current_user
                                                                 ).first()
        if type_operation:
            form.title.data = type_operation.title
            form.content.data = type_operation.content
            if type_operation.type_operation == 1:
                form.type_operation.data = 'Приход'
            elif type_operation.type_operation == 2:
                form.type_operation.data = 'Расход'
            else:
                form.type_operation.data = 'Универсал'

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.id == id,
                                                                 Type_of_operation.user == current_user
                                                                 ).first()
        if type_operation:
            type_operation.title = form.title.data
            type_operation.content = form.content.data
            if form.type_operation.data == 'Приход':
                type_operation.type_operation = 1
            elif form.type_operation.data == 'Расход':
                type_operation.type_operation = 2
            else:
                type_operation.type_operation = 3
            db_sess.commit()
            return redirect('/type_operation_table')
        else:
            abort(404)
    return render_template('type_operation.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/owner_money/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_owner(id):
    form = Owner_moneyForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        owner_money = db_sess.query(Owner_money).filter(Owner_money.id == id,
                                                        Owner_money.user == current_user
                                                        ).first()
        if owner_money:
            form.title.data = owner_money.title
            form.content.data = owner_money.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        owner_money = db_sess.query(Owner_money).filter(Owner_money.id == id,
                                                        Owner_money.user == current_user
                                                        ).first()
        if owner_money:
            owner_money.title = form.title.data
            owner_money.content = form.content.data
            db_sess.commit()
            return redirect('/owner_money_table')
        else:
            abort(404)
    return render_template('cards.html',
                           title='Редактирование owner',
                           form=form
                           )


@app.route('/resource/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_resource(id):
    form = ResourceForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        resource = db_sess.query(Resource).filter(Resource.id == id,
                                                  Resource.user == current_user
                                                  ).first()
        if resource:
            form.title.data = resource.title
            form.content.data = resource.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        resource = db_sess.query(Resource).filter(Resource.id == id,
                                                  Resource.user == current_user
                                                  ).first()
        if resource:
            resource.title = form.title.data
            resource.content = form.content.data
            db_sess.commit()
            return redirect('/resource_table')
        else:
            abort(404)
    return render_template('resource.html',
                           title='Редактирование ресурса',
                           form=form
                           )


@app.route('/cards_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def cards_delete(id):
    db_sess = db_session.create_session()
    cards = db_sess.query(Cards).filter(Cards.id == id,
                                        Cards.user == current_user
                                        ).first()
    if cards:
        db_sess.delete(cards)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/cards_table')


@app.route('/type_operation_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def type_operation_delete(id):
    db_sess = db_session.create_session()
    type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.id == id,
                                                             Type_of_operation.user == current_user
                                                             ).first()
    if type_operation:
        db_sess.delete(type_operation)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/type_operation_table')


@app.route('/owner_money_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def owner_money_delete(id):
    db_sess = db_session.create_session()
    owner_money = db_sess.query(Owner_money).filter(Owner_money.id == id,
                                                    Owner_money.user == current_user
                                                    ).first()
    if owner_money:
        db_sess.delete(owner_money)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/owner_money_table')


@app.route('/resource_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def resource_delete(id):
    db_sess = db_session.create_session()
    resource = db_sess.query(Resource).filter(Resource.id == id,
                                              Resource.user == current_user
                                              ).first()
    if resource:
        db_sess.delete(resource)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/resource_table')


# Закончились справочники!
# Закончились справочники!
# Закончились справочники!
# Закончились справочники!
# Закончились справочники!


@app.route('/operations', methods=['GET', 'POST'])
@login_required
def add_operation():
    form = OperationForm()

    db_sess = db_session.create_session()
    cards = db_sess.query(Cards).filter(Cards.user_id == current_user.id)
    type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.user_id == current_user.id). \
        order_by(desc(Type_of_operation.type_operation))
    form.card.choices = [(i.id, f'{i.title}') for i in cards]
    form.card_from.choices = [(i.id, i.title) for i in cards]
    form.card_to.choices = [(i.id, i.title) for i in cards]
    form.type_operation.choices = [(i.type_operation, f'{i.title} (Тип - {i.type_operation})') for i in type_operation]

    if form.validate_on_submit():
        create_engine('sqlite:///some.db', connect_args={'timeout': 10000})
        con = sqlite3.connect('db/family_bud.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT MAX(id) from operations""").fetchone()
        cur.close()

        operation = Operations()
        operation.type_operation_id = form.type_operation.data
        operation.created_date = form.date_time.data

        current_user.operations.append(operation)
        db_sess.merge(current_user)

        sub_operation = Sub_operation()
        print(form.type_operation.data)
        if form.type_operation.data == '1':
            sub_operation.prihod = form.sum.data if form.sum.data != '' else 0
            sub_operation.rashod = 0
        elif form.type_operation.data == '2':
            sub_operation.prihod = 0
            sub_operation.rashod = form.sum.data if form.sum.data != '' else 0
        else:
            sub_operation.prihod = 0
            sub_operation.rashod = 0

        sub_operation.id_operation = result[0] + 1 if result[0] is not None else 1
        sub_operation.id_cards = form.card.data
        sub_operation.user_id = current_user.id
        card = db_sess.query(Cards).filter(Cards.id == sub_operation.id_cards).first()
        card.balance += float(str(sub_operation.prihod).replace(',', '.')) if ',' in str(sub_operation.prihod)\
            else float(sub_operation.prihod)
        card.balance -= float(str(sub_operation.rashod).replace(',', '.')) if ',' in str(sub_operation.rashod)\
            else float(sub_operation.rashod)

        current_user.sub_operations.append(sub_operation)

        db_sess.merge(current_user)
        db_sess.commit()

        return redirect('/operations_table')
    return render_template('operations.html', title='Добавление операции',
                           form=form)


@app.route('/operations_table')
def get_operations_table():
    db_sess = db_session.create_session()
    operations = db_sess.query(Operations).filter(Operations.user_id == current_user.id)
    type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.user_id == current_user.id)
    cards = db_sess.query(Cards).filter(Cards.user_id == current_user.id)
    sub_operation = db_sess.query(Sub_operation).filter(Sub_operation.user_id == current_user.id)
    return render_template("operations_table.html", operations=operations, type_operation=type_operation,
                           cards=cards, sub_operation=sub_operation)


@app.route('/operations_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def operation_delete(id):
    db_sess = db_session.create_session()
    operations = db_sess.query(Operations).filter(Operations.id == id,
                                                  Operations.user == current_user
                                                  ).first()
    sub_operations = db_sess.query(Sub_operation).filter(Sub_operation.id == id == Operations.id,
                                                         Sub_operation.user == current_user
                                                         ).first()
    card = db_sess.query(Cards).filter(Cards.id == sub_operations.id_cards, Cards.user_id == current_user.id).first()
    if operations and sub_operations and card:
        db_sess.delete(operations)
        db_sess.delete(sub_operations)
        card.balance -= sub_operations.prihod
        card.balance += sub_operations.rashod
        db_sess.commit()
    else:
        abort(404)
    return redirect('/operations_table')


@app.route('/operations/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_operation(id):
    form = OperationForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        cards = db_sess.query(Cards).filter(Cards.user_id == current_user.id)
        type_operation = db_sess.query(Type_of_operation).filter(Type_of_operation.user_id == current_user.id).\
            order_by(Type_of_operation.type_operation)
        form.card.choices = [(i.id, i.title) for i in cards]
        form.type_operation.choices = [(i.id, i.title) for i in type_operation]
        operation = db_sess.query(Operations).filter(Operations.id == id,
                                                     Operations.user == current_user
                                                     ).first()
        sub_operation = db_sess.query(Sub_operation).filter(Sub_operation.id == id == operation.id,
                                                            Sub_operation.user == current_user).first()

        if operation and sub_operation:
            form.type_operation.data = operation.type_operation_id
            form.date_time.data = operation.created_date
            form.sum.data = sub_operation.rashod if sub_operation.rashod != 0 else sub_operation.prihod
            form.card.data = sub_operation.id_cards
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        operation = db_sess.query(Operations).filter(Operations.id == id,
                                                     Operations.user == current_user
                                                     ).first()
        sub_operation = db_sess.query(Sub_operation).filter(Sub_operation.id == id == Operations.id,
                                                            Sub_operation.user == current_user).first()
        if operation and sub_operation:
            card = db_sess.query(Cards).filter(Cards.id == sub_operation.id_cards).first()
            card.balance -= float(sub_operation.prihod)
            card.balance += float(sub_operation.rashod)
            operation.type_operation_id = form.type_operation.data
            operation.created_date = form.date_time.data
            if form.type_operation.data == '1':
                sub_operation.prihod = form.sum.data if form.sum.data != '' else 0
                sub_operation.rashod = 0
            elif form.type_operation.data == '2':
                sub_operation.prihod = 0
                sub_operation.rashod = form.sum.data if form.sum.data != '' else 0
            else:
                pass
            sub_operation.id_cards = form.card.data
            sub_operation.user_id = current_user.id
            card = db_sess.query(Cards).filter(Cards.id == sub_operation.id_cards).first()
            card.balance += float(sub_operation.prihod)
            card.balance -= float(sub_operation.rashod)

            db_sess.commit()
            return redirect('/operations_table')
        else:
            abort(404)
    return render_template('operations.html',
                           title='Редактирование операции',
                           form=form,
                           )


@app.route('/reload_cards_balance')
def reload_cards_balance():
    db_sess = db_session.create_session()
    cards = db_sess.query(Cards).filter(Cards.user_id == current_user.id)
    sub_operation = db_sess.query(Sub_operation).filter(Sub_operation.user_id == current_user.id)
    for i in cards:
        i.balance = 0
    for i in cards:
        for j in sub_operation:
            if j.id_cards == i.id:
                i.balance += j.prihod
                i.balance -= j.rashod
    db_sess.commit()
    return redirect('/cards_table')



if __name__ == '__main__':
    main()

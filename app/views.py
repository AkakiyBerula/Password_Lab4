from app import *
from app import db, SQLAlchemy, mail
from app.models import User
from app.forms import RegistrationForm, LoginForm, AuthorizationForm
from re import match
from random import randint
from http import cookies
from captcha.image import ImageCaptcha
from random import randint

@app.route("/users")
def users():
    all_users = User.query.all()
    flag = True
    if len(all_users) == 0:
        flash("Користувачі відсутні у базі даних.", category= "warning")
        flag = False
    resp = make_response(render_template('users.html', all_users = all_users, title = "Users", flag = flag))
    resp.set_cookie('used_attempts', '0')
    return resp

def generate_code():
    return str(randint(10 ** 7, 10 ** 8 - 1))

def generate_captcha_text():
    text = ""
    length_gen = randint(5, 8)
    for i in range(length_gen):
        choose_gen = randint(1, 2)
        if choose_gen == 1:
            text += chr(randint(97, 122))
        elif choose_gen == 2:
            text += str(randint(0, 9))
    return text

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    image = ImageCaptcha(width = 280, height = 90)
    captcha_text = generate_captcha_text()
    image.write(captcha_text, 'app/static/img/CAPTCHA.png')
    counter = int(request.cookies.get('used_attempts', 0))
    if counter >= 6:
        return render_template('failed.html', title='Register')
    form.captcha_user.data = session["captcha_text"]
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username = username, email = email, password = password)
        session['username'] = username
        session['email'] = email
        session['password'] = password
        session['code'] = generate_code()
        return redirect(url_for('me'))
    else:
        counter += 1
    session["captcha_text"] = captcha_text
    resp = make_response(render_template('register.html', form=form, captcha_image = 'CAPTCHA.png', title = 'Register'))
    resp.set_cookie('used_attempts', str(counter))
    print(counter)
    return resp



@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        dataEmail = User.query.filter_by(email = email).first()
        if dataEmail is None or dataEmail.verify_password(password) == False:
            flash('Відсутній обліковий запис. Зареєструйте свій аккаунт.', 
            category ='warning') 
            return redirect(url_for('register'))   
        else:
            flash("Авторизація пройшла успішно!", category = 'success')
    return make_response(render_template('login.html', form=form, title='Login')).set_cookie('used_attempts', '0')


@app.route("/kek", methods = ['GET', 'POST'])
def me():
    form = AuthorizationForm()
    username = session['username']
    email = session['email']
    password = session['password']
    code = session['code']
    msg = Message('Hello from the other side!', 
                sender = 'vlad5dyakun@gmail.com', 
                recipients = [email])
    msg.subject = "Ваш код для підтвердження"
    msg.body = f"Якщо це ваш аккаунт, то введіть код для підтвердження авторизації \nКод підтвердження: {code}"
    mail.send(msg)
    print(session['code'] * 2)
    if form.validate_on_submit():
        my_code = form.code.data
        print(my_code)
        print(code)
        if my_code == code:
            user = User(username = username, email = email, password = password)
            db.session.add(user)
            db.session.commit()
            flash(f'Створено аккаунт для користувача {username}!', category = 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Код не підтверджено! Надіслано інший код!!!', category = 'warning')
            session['code'] = generate_code()
            return redirect(url_for('me'))
    return render_template('double_auth.html', form=form, title='Login')

from flask_app import app
from flask import redirect,session,render_template,request,flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'logged_in' in session:
        if session['logged_in'] == True:
            return redirect('/wall')
    else:
        return render_template('index.html')

@app.route('/wall')
def wall():
    if not 'logged_in' in session:
        return redirect('/')
    data = { 'id' : session['user_id'] }
    user = User.get_user_by_id(data)
    posts = Post.show_all_posts()
    return render_template('wall.html', user=user, posts=posts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    email = { 'email': request.form['email']}
    if not User.unique_email(email):
        flash('Email is already registered', 'register')
        return redirect('/')
    if not User.user_vald_register(request.form):
        return redirect('/')
    if request.form['password'] != request.form['confirm_password']:
        flash('Passwords Do Not Match', 'register')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    session['logged_in'] = True
    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['logged_in'] = True
    return redirect('/wall')
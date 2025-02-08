
from flask import Flask, redirect, render_template, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'

connect_db(app)

with app.app_context():
  db.create_all()

@app.route('/')
def home():
  """redirect to /register"""
  return redirect('/register')

@app.route('/register', methods = ["GET", "POST"])
def register():
  """show and handle register form"""
  form = RegisterForm()
  if form.validate_on_submit():
    hashed_pass = bcrypt.generate_password_hash(form.password.data)
    hashed_utf8 = hashed_pass.decode("utf8")
    user = User(
      username = form.username.data,
      password = hashed_utf8,
      email = form.email.data,
      first_name = form.first_name.data,
      last_name = form.last_name.data
    )

    db.session.add(user)
    db.session.commit()

    session["username"] = user.username

    return redirect(f"/users/{ user.username }")
  return render_template('form_template.html', form = form, title = "User Registration")

@app.route('/login', methods = ["GET", "POST"])
def login():
  """show and handle login form"""
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      session["username"] = user.username
      return redirect(f"/users/{ user.username }")
    else:
      form.username.errors = ["Invalid username/password."]
      return render_template("form_template.html", form = form, title = "Login")
  return render_template("form_template.html", form = form, title = "Login")

@app.route('/logout')
def logout():
  """log user out"""

  session.pop("username")
  return redirect('/')

@app.route('/users/<username>')
def user(username):
  """show secret page"""
  if 'username' in session:
    user = User.query.get_or_404(username)
    return render_template('users.html', user = user)
  flash("you are not authorized to see this page")
  return redirect('login')

@app.route('/users/<username>/feedback/add', methods = ["GET", "POST"])
def add_feedback(username):
  if 'username' in session and session["username"] == username:
    form = FeedbackForm()
    if form.validate_on_submit():
      feedback = Feedback(
        title = form.title.data,
        content = form.content.data,
        username = username
      )
      db.session.add(feedback)
      db.session.commit()
      return redirect(f"/users/{ username }")
    return render_template("form_template.html", form = form, title = "New Feedback")
  flash("you are not authorized to see this page")
  return redirect('/')

@app.route('/users/<username>/delete', methods = ["POST"])
def delete_user(username):
  """remove user from app"""
  if 'username' in session and session["username"] == username:
    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()

    session.pop("username")
  return redirect("/")

@app.route('/feedback/<int:id>/update', methods = ["POST"])
def edit_feedback(id):
  """edit feedback"""
  feedback = Feedback.query.get_or_404(id)
  if 'username' in session and session["username"] == feedback.users.username:
    form = FeedbackForm(feedback)
    if form.validate_on_submit():
      feedback.title = form.title.data
      feedback.content = form.content.data

      db.session.add(feedback)
      db.session.commit()

      return redirect(f"/users/{ feedback.users.username }")
    return render_template("form_template.html", form = form, title = "Edit Feedback")
  flash("you are not authorized to see this page")
  return redirect('/')

@app.route('/feedback/<int:id>/delete')
def delete_feedback(id):
  """remove a feedback from the app"""
  feedback = Feedback.query.get_or_404(id)
  if 'username' in session and session["username"] == feedback.users.username:
    db.session.delete(feedback)
    db.session.commit()
  return redirect(f"/users/{ feedback.users.username }")

@app.route('/clear')
def clear():
  db.drop_all()
  db.create_all()
  return redirect('/login')

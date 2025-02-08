from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional, Length, URL

class RegisterForm(FlaskForm):
  """form for adding new user to database"""

  username = StringField("Username", 
                         validators=[InputRequired(), Length(max=20)])
  password = PasswordField("Password", validators=[InputRequired()])
  email = EmailField("Email",
                      validators=[InputRequired(), Length(max=50)])
  first_name = StringField("First name",
                           validators=[InputRequired(), Length(max=30)])
  last_name = StringField("Last name",
                          validators=[InputRequired(), Length(max=30)])
  
class LoginForm(FlaskForm):
  """form for loging into an existing user"""

  username = StringField("Username",
                         validators=[InputRequired(), Length(max=20)])
  password = PasswordField("Password",
                           validators=[InputRequired()])
  
class FeedbackForm(FlaskForm):
  """form for creating new user feedback"""

  title = StringField("Title",
                      validators=[InputRequired(), Length(max=(100))])
  content = StringField("Content", validators=[InputRequired()])
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)

    password = db.Column(db.String(80), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Movie_or_Game = db.Column(db.String(20), nullable=False,)
    Movie_or_Game_Name = db.Column(db.String(20), nullable=False, )
    Review_Date = db.Column(db.Date, nullable=False, )
    Your_Rating = db.Column(db.Integer, nullable=False, )
    Review_Text = db.Column(db.String(20), nullable=False, )

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

    class DashboardForm(FlaskForm):
        Movie_or_Game = StringField(validators=[
            InputRequired(), Length(min=1, max=20)],
            render_kw={"placeholder": "Movie_or_Game"})  # Movie_or_Game field with validation
        Movie_or_Game_Name = StringField(validators=[
            InputRequired(), Length(min=1, max=20)],
            render_kw={"placeholder": "Movie_or_Game_Name"})  # Movie_or_Game field with validation
        Review_Date=DateField(validators=[
            InputRequired()],
            render_kw={"placeholder": "Review_Date"})  # Movie_or_Game field with validation
        Your_Rating = IntegerField(validators=[
            InputRequired()],
            render_kw={"placeholder": "Your_Rating"})  # Movie_or_Game field with validation
        Review_Text = StringField(validators=[
            InputRequired(), Length(min=1, max=20)],
            render_kw={"placeholder": "Review_Text"})  # Movie_or_Game field with validation

        submit = SubmitField('Submit Review')  # Submit button


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])

def dashboard():
    form=Review()
    new_review = Review(Movie_or_Game=form.Movie_or_Game.data, Moview_or_Game_Name=form.Movie_or_Game_Name.data,
                            Review_Date=form.Review_Date.data, Your_Rating=form.Your_Rating.data, Review_Text=form.Review_Text.data)
    db.session.add(new_review)
    db.session.commit()

    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
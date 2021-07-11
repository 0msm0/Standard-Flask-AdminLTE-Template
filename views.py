from flask import render_template, request, redirect, session, flash, url_for
# from flask_login import logout
from models import User
import functools
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=120)
    
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("auth_login", next=request.url))
        return func(*args, **kwargs)

    return secure_function

@app.route('/')
@app.route('/dashboard')
@login_required
def index():
    return render_template("homepage/dashboard.html", name=session.get("email", "Unknown"))

@app.route('/datatable')
@login_required
def datatable():
    return render_template("homepage/datatable.html", name=session["email"])

@app.route('/login', methods=["POST", "GET"])
def auth_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        next_url = request.form.get("next")
        session["email"] = email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='success')
                if next_url:
                    return redirect(next_url)
                return redirect(url_for("index"))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("auth/login.html")

@app.route('/register', methods=["POST", "GET"])
def auth_register():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return render_template('auth/login.html')

    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop("email")
    return redirect(url_for('auth_login'))

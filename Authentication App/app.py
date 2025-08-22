from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_user_file(username):
    return f"{username}.txt"

def user_exists(username):
    return os.path.isfile(get_user_file(username))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        age = request.form['age']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if user_exists(username):
            flash('Username already exists.')
            return redirect(url_for('register'))
        if "@gmail.com" not in email:
            flash('Email must be a Gmail address.')
            return redirect(url_for('register'))
        if not age.isdigit() or not (12 < int(age) < 100):
            flash('Age must be between 13 and 99.')
            return redirect(url_for('register'))
        if len(password) < 8 or len(password) > 16 or password.isalpha() or password.isdigit():
            flash('Password must be 8-16 characters and contain letters and numbers.')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        with open(get_user_file(username), 'w') as f:
            f.write(f"{username}\n{email}\n{age}\n{password}")
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not user_exists(username):
            flash('That username does not exist.')
            return redirect(url_for('login'))

        with open(get_user_file(username), 'r') as f:
            lines = f.read().splitlines()
            stored_username, stored_email, stored_age, stored_password = lines

        if email != stored_email:
            flash('Incorrect email.')
            return redirect(url_for('login'))
        if password != stored_password:
            flash('Incorrect password.')
            return redirect(url_for('login'))

        # Pass all details to the dashboard
        return render_template(
            'dashboard.html',
            username=stored_username,
            email=stored_email,
            age=stored_age
        )

    return render_template('login.html')
@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
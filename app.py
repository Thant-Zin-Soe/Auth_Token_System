from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import save_user, verify_user, generate_token, validate_token
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session

#  Home Route
@app.route('/')
def home():
    return redirect(url_for('login'))

#  Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if save_user(email, password):
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User already exists.', 'danger')
    return render_template('register.html')

#  Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if verify_user(email, password):
            token = generate_token(email)
            session['token'] = token
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

# Dashboard (Show Token)
import jwt

@app.route('/dashboard')
def dashboard():
    token = session.get('token', None)
    access = None

    if token:
        try:
            decoded = jwt.decode(token, 'supersecretkey', algorithms=['HS256'])
            access = decoded.get('access', 'user')
        except jwt.ExpiredSignatureError:
            flash("Token expired. Please log in again.", 'warning')
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            flash("Invalid token.", 'danger')
            return redirect(url_for('login'))

    return render_template('dashboard.html', token=token, access=access)


# ✅ Token Validation
@app.route('/validate', methods=['GET', 'POST'])
def validate():
    message = None
    if request.method == 'POST':
        token_input = request.form['token']
        message = validate_token(token_input)
    return render_template('validate.html', message=message)

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# ▶️ Run the app
if __name__ == '__main__':
    app.run(debug=True)

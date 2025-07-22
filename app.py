import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,  User

app = Flask(__name__)


# Use Railway database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Create tables on startup
with app.app_context():
    db.create_all()
    try:
        db.session.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed:", e)

# Secret key
app.secret_key = 'kenya_healthcare_secret_2023_@medifind!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("❌ Passwords do not match!", "error")
            return redirect(url_for('register'))

        # Check if email is already used
        if User.query.filter_by(email=email).first():
            flash("⚠️ Email already registered!", "error")
            return redirect(url_for('register'))

        # Hash and save user
        hashed_password = generate_password_hash(password)
        new_user = User(full_name=full_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Store user session
            session['user_id'] = user.id
            session['user_name'] = user.full_name
            flash("✅ Login successful!", "success")
            return redirect(url_for('dashboard'))  # Redirects to dashboard.html
        else:
            flash("❌ Invalid email or password", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/test-db')
def test_db():
    result = db.session.execute(text("SELECT 1")).scalar()
    return f"Database OK: {result}"

if __name__ == '__main__':
    print("Starting MediFind backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)

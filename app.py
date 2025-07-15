import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Hospital, User

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

# Hardcoded diseases only
DISEASES = [
    'Malaria', 'Diabetes', 'Hypertension', 'HIV/AIDS', 'Tuberculosis',
    'Pneumonia', 'Stroke', 'Maternal Emergencies', 'Kidney Disease', 'Cancer',
    'Typhoid', 'Cholera', 'Bilharzia', 'Dengue Fever'
]

# Kenya counties for dropdowns
KENYA_COUNTIES = [
    'Baringo', 'Bomet', 'Bungoma', 'Busia', 'Elgeyo-Marakwet', 'Embu', 'Garissa',
    'Homa Bay', 'Isiolo', 'Kajiado', 'Kakamega', 'Kericho', 'Kiambu', 'Kilifi',
    'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui', 'Kwale', 'Laikipia', 'Lamu', 'Machakos',
    'Makueni', 'Mandera', 'Meru', 'Migori', 'Marsabit', 'Mombasa', 'Muranga', 'Nairobi',
    'Nakuru', 'Nandi', 'Narok', 'Nyamira', 'Nyandarua', 'Nyeri', 'Samburu', 'Siaya',
    'Taita-Taveta', 'Tana River', 'Tharaka-Nithi', 'Trans Nzoia', 'Turkana', 'Uasin Gishu',
    'Vihiga', 'Wajir', 'West Pokot'
]

# Home page with form
@app.route('/')
def index():
    return render_template('index.html', counties=KENYA_COUNTIES)

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

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    hospitals = Hospital.query.filter_by(status='Approved').all()

    return render_template('dashboard.html', user=user, hospitals=hospitals)



@app.route('/search', methods=['GET', 'POST'])
def search():
    condition = request.args.get('condition', '').strip().lower()
    location = request.args.get('location', '').strip().lower()

    query = Hospital.query

    if location:
        query = query.filter(Hospital.county.ilike(f"%{location}%"))
    
    if condition:
        query = query.filter(Hospital.specialties.ilike(f"%{condition}%"))

    results = query.all()

    if not results:
        flash("⚠️ No hospitals found matching your search criteria.", "warning")

    return render_template("search_results.html", hospitals=results)


# Form submission route
@app.route('/submission', methods=['POST', 'GET'])
def submission():

    if request.method == 'GET':
        return render_template('submission.html', counties=KENYA_COUNTIES)
    data = request.form

    facilities = []
    if '24hr-service' in data:
        facilities.append("24hr")
    if 'nhif-accepted' in data:
        facilities.append("NHIF")
    if 'emergency-services' in data:
        facilities.append("Emergency")
    if 'maternity-services' in data:
        facilities.append("Maternity")

    hospital = Hospital(
        hospital_name=data.get("hospital-name"),
        county=data.get("county"),
        address=data.get("physical-address"),
        phone=data.get("phone"),
        alt_phone=data.get("alt-phone"),
        contact_person=data.get("contact-person"),
        email=data.get("contact-email"),
        facilities=",".join(facilities),
        specialties=data.get("specialties"),
            
    )

    db.session.add(hospital)
    db.session.commit()

    flash("✅ Hospital registered successfully!", "success")
    return redirect(url_for('submission'))

# Simple confirmation page

@app.route('/system_admin')
def system_admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))  # protect page

    pending_hospitals = Hospital.query.filter_by(status='Pending').all()
    approved_hospitals = Hospital.query.filter_by(status='Approved').all()

    return render_template(
        'system_admin.html',
        pending_hospitals=pending_hospitals,
        approved_hospitals=approved_hospitals
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Hardcoded admin credentials
    admin_username = "admin@medifind.com"
    admin_password = "admin123"

    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        if input_username == admin_username and input_password == admin_password:
            session['admin_logged_in'] = True
            flash("✅ Admin logged in successfully!", "success")
            return redirect(url_for('system_admin'))
        else:
            flash("❌ Invalid admin credentials", "error")
            return redirect(url_for('admin'))

    return render_template('admin_login.html')

@app.route('/approve/<int:hospital_id>')
def approve_hospital(hospital_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    hospital = Hospital.query.get_or_404(hospital_id)
    hospital.status = 'Approved'
    db.session.commit()
    flash("✅ Hospital approved", "success")
    return redirect(url_for('system_admin'))

@app.route('/reject/<int:hospital_id>')
def reject_hospital(hospital_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    hospital = Hospital.query.get_or_404(hospital_id)
    hospital.status = 'Rejected'
    db.session.commit()
    flash("⚠️ Hospital rejected", "warning")
    return redirect(url_for('system_admin'))

@app.route('/update_hospital/<int:hospital_id>', methods=['GET', 'POST'])
def update_hospital(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)

    if request.method == 'POST':
        hospital.hospital_name = request.form['name']
        hospital.county = request.form['county']
        hospital.phone = request.form['phone']
        hospital.email = request.form['email']
        hospital.specialties = request.form['specialties']
        hospital.facilities = request.form['facilities']
        db.session.commit()
        flash('✅ Hospital details updated successfully.', 'success')
        return redirect(url_for('system_admin'))

    return render_template('update_hospital.html', hospital=hospital, counties=KENYA_COUNTIES)


@app.route('/logout-admin')
def logout_admin():
    session.pop('admin_logged_in', None)
    flash("👋 Admin logged out.", "info")
    return redirect(url_for('admin'))

# DB Test
@app.route('/test-db')
def test_db():
    result = db.session.execute(text("SELECT 1")).scalar()
    return f"Database OK: {result}"

if __name__ == '__main__':
    print("Starting MediFind backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)

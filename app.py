import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db, Hospital

app = Flask(__name__)

# Database configuration (fix render database URL format)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://', 1)
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

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/search_results')
def search():
    return render_template('search_results.html')

# Form submission route
@app.route('/submission', methods=['POST'])
def register_hospital():
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
@app.route('/submission')
def submission():
    return render_template('submission.html')

# DB Test
@app.route('/test-db')
def test_db():
    result = db.session.execute(text("SELECT 1")).scalar()
    return f"Database OK: {result}"

if __name__ == '__main__':
    print("Starting MediFind backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)

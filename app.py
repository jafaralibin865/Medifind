import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Important addition

app = Flask(__name__)
# Fix the PostgreSQL URL format
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TEST CONNECTION
@app.route("/test-db")
def test_db():
    from sqlalchemy import text
    result = db.session.execute(text("SELECT 1")).scalar()
    return f"Database OK: {result}"
try:
    with app.app_context():
        db.session.execute(text('SELECT 1'))  # Now properly wrapped
    print("✅ Database connection successful!")
except Exception as e:
    print("❌ Database connection failed:", e)
app.secret_key = 'kenya_healthcare_secret_2023_@medifind!'

# Hardcoded data for frontend testing
HOSPITALS = [
    {
        'id': 1,
        'name': 'Kenyatta National Hospital',
        'location': 'Hospital Rd, Nairobi',
        'county': 'Nairobi',
        'contact': '+254 20 272 6300',
        'is_24hr': True,
        'is_nhif_accepted': True,
        'verification_status': 'verified',
        'diseases': ['Cancer', 'Stroke', 'Kidney Disease', 'Maternal Emergencies']
    },
    {
        'id': 2,
        'name': 'Moi Teaching and Referral Hospital',
        'location': 'Nandi Rd, Eldoret',
        'county': 'Uasin Gishu',
        'contact': '+254 53 203 3471',
        'is_24hr': True,
        'is_nhif_accepted': True,
        'verification_status': 'verified',
        'diseases': ['Diabetes', 'Hypertension', 'Cancer', 'Kidney Disease']
    },
    {
        'id': 3,
        'name': 'Coast General Hospital',
        'location': 'Mombasa-Malindi Road',
        'county': 'Mombasa',
        'contact': '+254 41 231 3578',
        'is_24hr': True,
        'is_nhif_accepted': True,
        'verification_status': 'pending',
        'diseases': ['Malaria', 'Typhoid', 'Pneumonia', 'Cholera']
    }
]

DISEASES = [
    'Malaria', 'Diabetes', 'Hypertension', 'HIV/AIDS', 'Tuberculosis',
    'Pneumonia', 'Stroke', 'Maternal Emergencies', 'Kidney Disease', 'Cancer',
    'Typhoid', 'Cholera', 'Bilharzia', 'Dengue Fever'
]

ADMINS = {
    'knh_admin': {
        'password': 'admin123',
        'hospital_id': 1
    },
    'mtrh_admin': {
        'password': 'admin123',
        'hospital_id': 2
    }
}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submission')
def submission():
    return render_template('submission.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    condition = request.form.get('condition', '')
    location = request.form.get('location', '')
    results = []
    
    if request.method == 'POST' and condition and location:
        # Filter hospitals based on condition and location
        condition_lower = condition.lower()
        location_lower = location.lower()
        
        for hospital in HOSPITALS:
            # Check if hospital treats the condition
            treats_condition = any(condition_lower in disease.lower() 
                                   for disease in hospital['diseases'])
            
            # Check if hospital is in the location
            in_location = (location_lower in hospital['county'].lower() or 
                           location_lower in hospital['location'].lower())
            
            if treats_condition and in_location:
                results.append(hospital)
    
    return render_template('search.html', diseases=DISEASES, results=results, 
                           condition=condition, location=location)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in ADMINS and ADMINS[username]['password'] == password:
            hospital_id = ADMINS[username]['hospital_id']
            hospital = next((h for h in HOSPITALS if h['id'] == hospital_id), None)
            
            if hospital:
                session['admin_id'] = username
                session['hospital_id'] = hospital_id
                session['username'] = username
                session['hospital_name'] = hospital['name']
                return redirect(url_for('admin_dashboard'))
        
        error = "Invalid credentials. Please try again."
    
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    hospital_id = session['hospital_id']
    hospital = next((h for h in HOSPITALS if h['id'] == hospital_id), None)
    
    if not hospital:
        flash('Hospital not found', 'danger')
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html', hospital=hospital, 
                           all_diseases=DISEASES, 
                           treated_diseases=hospital['diseases'])

@app.route('/admin/update', methods=['POST'])
def admin_update():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    hospital_id = session['hospital_id']
    hospital = next((h for h in HOSPITALS if h['id'] == hospital_id), None)
    
    if not hospital:
        flash('Hospital not found', 'danger')
        return redirect(url_for('admin_login'))
    
    # Update hospital info
    hospital['name'] = request.form['name']
    hospital['location'] = request.form['location']
    hospital['county'] = request.form['county']
    hospital['contact'] = request.form['contact']
    hospital['is_24hr'] = 'is_24hr' in request.form
    hospital['is_nhif_accepted'] = 'is_nhif_accepted' in request.form
    
    # Update treated diseases
    selected_diseases = request.form.getlist('diseases')
    hospital['diseases'] = [d for d in DISEASES if d in selected_diseases]
    
    flash('Hospital information updated successfully! (Changes are temporary)', 'success')
    return redirect(url_for('admin_dashboard'))

# Kenya counties list for reference
KENYA_COUNTIES = [
    'Baringo', 'Bomet', 'Bungoma', 'Busia', 'Elgeyo-Marakwet', 'Embu', 'Garissa', 
    'Homa Bay', 'Isiolo', 'Kajiado', 'Kakamega', 'Kericho', 'Kiambu', 'Kilifi', 
    'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui', 'Kwale', 'Laikipia', 'Lamu', 'Machakos', 
    'Makueni', 'Mandera', 'Meru', 'Migori', 'Marsabit', 'Mombasa', 'Muranga', 'Nairobi', 
    'Nakuru', 'Nandi', 'Narok', 'Nyamira', 'Nyandarua', 'Nyeri', 'Samburu', 'Siaya', 
    'Taita-Taveta', 'Tana River', 'Tharaka-Nithi', 'Trans Nzoia', 'Turkana', 'Uasin Gishu', 
    'Vihiga', 'Wajir', 'West Pokot'
]

if __name__ == '__main__':
    print("Starting frontend-focused MediFind Kenya application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
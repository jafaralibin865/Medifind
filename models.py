from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Hospital model
class Hospital(db.Model):
    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    hospital_name = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=False)

    # Contact Info
    phone = db.Column(db.String(15), nullable=False)
    alt_phone = db.Column(db.String(15))
    contact_person = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Services / Facilities
    facilities = db.Column(db.String(300))  # e.g. "NHIF,24hr,Maternity"
    specialties = db.Column(db.Text)        # e.g. "Pediatrics,Cardiology"

    status = db.Column(db.String(20), default='Pending')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Hospital {self.hospital_name} in {self.county}>"

# ✅ User model – moved out of Hospital
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    hospitals = db.relationship('Hospital', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.full_name}>"

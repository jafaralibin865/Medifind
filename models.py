# models.py

from flask_sqlalchemy import SQLAlchemy

# Create the database instance
db = SQLAlchemy()

# Define the Hospital table structure
class Hospital(db.Model):
    __tablename__ = 'hospitals'  # optional, but recommended

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
    facilities = db.Column(db.String(300))  # comma-separated: "NHIF,24hr,Maternity"
    specialties = db.Column(db.Text)        # comma-separated: "Pediatrics,Cardiology"

    # Geolocation
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f"<Hospital {self.hospital_name} in {self.county}>"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ✅ User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(200), nullable=False)

  
    def __repr__(self):
        return f"<User {self.full_name}>"

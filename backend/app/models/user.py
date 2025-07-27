from app.extensions import db
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Add this line
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(
        Enum('Developer', 'School Admin', 'Teacher', name='user_role_enum'),
        default='Teacher',
        nullable=False
    )
    # Add Foreign Key to School table
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)
    
    # Add relationship to School model
    school = db.relationship('School', back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'
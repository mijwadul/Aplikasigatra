from app.extensions import db

class Class(db.Model):
    __tablename__ = 'class'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.String(20), nullable=False) # e.g., "7", "8", "9"
    
    # Foreign Key to School
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    
    # Relationship to School
    school = db.relationship('School', back_populates='classes')

    def __repr__(self):
        return f'<Class {self.name}>'
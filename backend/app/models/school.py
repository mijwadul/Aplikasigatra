from app.extensions import db

class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    
    users = db.relationship('User', back_populates='school')
    classes = db.relationship('Class', back_populates='school', cascade="all, delete-orphan") # Add this line

    def __repr__(self):
        return f'<School {self.name}>'
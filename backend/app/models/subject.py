# backend/app/models/subject.py

from app.extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    is_custom = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_custom': self.is_custom
        }

    def __repr__(self):
        return f'<Subject {self.name}>'
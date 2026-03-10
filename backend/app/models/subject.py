# backend/app/models/subject.py

from app.extensions import db
from sqlalchemy import UniqueConstraint

class Subject(db.Model):
    __tablename__ = 'subjects'
    __table_args__ = (UniqueConstraint('name', 'school_level', name='uq_subject_name_level'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_custom = db.Column(db.Boolean, default=False, nullable=False)
    # school_level: 'SD/MI', 'SMP/MTs', 'SMA/MA', atau None untuk custom (tampil di semua level)
    school_level = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_custom': self.is_custom,
            'school_level': self.school_level
        }

    def __repr__(self):
        return f'<Subject {self.name}>'
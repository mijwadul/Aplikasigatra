from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Class
from app.utils.decorators import token_required

class_bp = Blueprint('class_bp', __name__)

@class_bp.route('/api/classes', methods=['GET'])
@token_required
def get_classes(current_user):
    # ... (GET function remains the same)
    if current_user.role == 'Developer':
        classes = Class.query.all()
    elif current_user.school_id:
        classes = Class.query.filter_by(school_id=current_user.school_id).all()
    else:
        classes = []
    class_list = [{"id": c.id, "name": c.name, "grade_level": c.grade_level, "school_id": c.school_id} for c in classes]
    return jsonify(class_list)

@class_bp.route('/api/classes', methods=['POST'])
@token_required
def create_class(current_user):
    # ... (POST function remains the same)
    if current_user.role not in ['Developer', 'School Admin']:
        return jsonify({"error": "Permission denied."}), 403
    data = request.get_json()
    if not data or not data.get('name') or not data.get('grade_level'):
        return jsonify({"error": "Name and grade level are required."}), 400
    school_id = current_user.school_id if current_user.role == 'School Admin' else data.get('school_id')
    if not school_id:
        return jsonify({"error": "School ID is required."}), 400
    new_class = Class(name=data['name'], grade_level=data['grade_level'], school_id=school_id)
    db.session.add(new_class)
    db.session.commit()
    return jsonify({"message": "Class created successfully.", "id": new_class.id}), 201

@class_bp.route('/api/classes/<int:class_id>', methods=['PUT'])
@token_required
def update_class(current_user, class_id):
    """Update a class."""
    cls = Class.query.get_or_404(class_id)
    
    # Permission check: User must be a developer or belong to the same school
    if current_user.role != 'Developer' and current_user.school_id != cls.school_id:
        return jsonify({"error": "Permission denied."}), 403
        
    data = request.get_json()
    cls.name = data.get('name', cls.name)
    cls.grade_level = data.get('grade_level', cls.grade_level)
    db.session.commit()
    return jsonify({"message": "Class updated successfully."})

@class_bp.route('/api/classes/<int:class_id>', methods=['DELETE'])
@token_required
def delete_class(current_user, class_id):
    """Delete a class."""
    cls = Class.query.get_or_404(class_id)

    # Permission check: User must be a developer or belong to the same school
    if current_user.role != 'Developer' and current_user.school_id != cls.school_id:
        return jsonify({"error": "Permission denied."}), 403
        
    db.session.delete(cls)
    db.session.commit()
    return jsonify({"message": "Class deleted successfully."})
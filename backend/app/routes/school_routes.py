from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import School
from app.utils.decorators import token_required

school_bp = Blueprint('school_bp', __name__)

@school_bp.route('/api/schools', methods=['GET'])
@token_required
def get_schools(current_user):
    """Get a list of all schools."""
    schools = School.query.all()
    school_list = [{"id": s.id, "name": s.name, "address": s.address} for s in schools]
    return jsonify(school_list)

@school_bp.route('/api/schools', methods=['POST'])
@token_required
def create_school(current_user):
    """Create a new school (Developer only)."""
    if current_user.role != 'Developer':
        return jsonify({"error": "Permission denied."}), 403
    
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "School name is required."}), 400

    if School.query.filter_by(name=data['name']).first():
        return jsonify({"error": "A school with this name already exists."}), 409

    new_school = School(name=data['name'], address=data.get('address'))
    db.session.add(new_school)
    db.session.commit()
    return jsonify({"message": "School created successfully.", "id": new_school.id}), 201

@school_bp.route('/api/schools/<int:school_id>', methods=['PUT'])
@token_required
def update_school(current_user, school_id):
    """Update a school's name and address (Developer only)."""
    if current_user.role != 'Developer':
        return jsonify({"error": "Permission denied."}), 403
        
    school = School.query.get_or_404(school_id)
    data = request.get_json()
    school.name = data.get('name', school.name)
    school.address = data.get('address', school.address) # Update the address
    db.session.commit()
    return jsonify({"message": "School updated successfully."})

@school_bp.route('/api/schools/<int:school_id>', methods=['DELETE'])
@token_required
def delete_school(current_user, school_id):
    """Delete a school (Developer only)."""
    if current_user.role != 'Developer':
        return jsonify({"error": "Permission denied."}), 403

    school = School.query.get_or_404(school_id)
    db.session.delete(school)
    db.session.commit()
    return jsonify({"message": "School deleted successfully."})
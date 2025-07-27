from flask import Blueprint, jsonify, request
from app.extensions import db, bcrypt
from app.models import User, School
from app.utils.decorators import token_required

user_mgmt_bp = Blueprint('user_mgmt_bp', __name__)

@user_mgmt_bp.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user):
    # ... (This function remains the same)
    if current_user.role == 'Developer':
        users = User.query.all()
    elif current_user.role == 'School Admin':
        if not current_user.school_id:
            return jsonify([{"id": current_user.id, "username": current_user.username, "email": current_user.email, "role": current_user.role, "school_id": current_user.school_id}])
        users = User.query.filter(
            (User.id == current_user.id) | 
            ((User.school_id == current_user.school_id) & (User.role == 'Teacher'))
        ).all()
    else:
        return jsonify({"error": "You do not have permission to access this resource."}), 403

    user_list = [{"id": u.id, "username": u.username, "email": u.email, "role": u.role, "school_id": u.school_id} for u in users]
    return jsonify(user_list)

@user_mgmt_bp.route('/api/users', methods=['POST'])
@token_required
def create_user(current_user):
    # ... (This function remains the same)
    if current_user.role not in ['Developer', 'School Admin']:
        return jsonify({"error": "Permission denied."}), 403
    data = request.get_json()
    if User.query.filter((User.email == data['email']) | (User.username == data['username'])).first():
        return jsonify({"error": "User with this email or username already exists."}), 409
    if current_user.role == 'School Admin' and data['role'] != 'Teacher':
        return jsonify({"error": "Admins can only create Teacher accounts."}), 403
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password, role=data['role'])
    if current_user.role == 'School Admin':
        new_user.school_id = current_user.school_id
    elif data.get('school_id'):
        new_user.school_id = data.get('school_id')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201

# --- NEW UPDATE ROUTE ---
@user_mgmt_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    user_to_update = User.query.get_or_404(user_id)
    
    # Check permissions
    if current_user.role == 'Teacher' and current_user.id != user_to_update.id:
        return jsonify({"error": "Permission denied."}), 403
    if current_user.role == 'School Admin' and not (current_user.id == user_to_update.id or (user_to_update.school_id == current_user.school_id and user_to_update.role == 'Teacher')):
        return jsonify({"error": "Permission denied."}), 403

    data = request.get_json()
    if 'email' in data and User.query.filter(User.email == data['email'], User.id != user_id).first():
        return jsonify({"error": "Email already in use."}), 409
    if 'username' in data and User.query.filter(User.username == data['username'], User.id != user_id).first():
        return jsonify({"error": "Username already in use."}), 409

    user_to_update.email = data.get('email', user_to_update.email)
    user_to_update.username = data.get('username', user_to_update.username)
    if data.get('password'):
        user_to_update.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Only Developers can change roles
    if current_user.role == 'Developer' and 'role' in data:
        user_to_update.role = data.get('role', user_to_update.role)
        
    db.session.commit()
    return jsonify({"message": "User updated successfully."})

# --- NEW DELETE ROUTE ---
@user_mgmt_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    user_to_delete = User.query.get_or_404(user_id)
    
    if current_user.id == user_to_delete.id:
        return jsonify({"error": "You cannot delete your own account."}), 400

    # Check permissions
    if current_user.role == 'Teacher':
        return jsonify({"error": "Permission denied."}), 403
    if current_user.role == 'School Admin' and not (user_to_delete.school_id == current_user.school_id and user_to_delete.role == 'Teacher'):
        return jsonify({"error": "Permission denied."}), 403

    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"message": "User deleted successfully."})
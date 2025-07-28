# backend/app/routes/class_routes.py

from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import School, Subject, User, Class
from app.utils.decorators import token_required

# Nama blueprint Anda adalah 'class_bp', kita akan tetap menggunakannya
class_bp = Blueprint('class_bp', __name__)

@class_bp.route('/api/classes/form-data', methods=['GET'])
@token_required
def get_form_data(current_user):
    """
    Mengirimkan data untuk form.
    - Untuk Admin, data sekolahnya otomatis.
    - Untuk Developer, mengirim daftar semua sekolah untuk dipilih.
    """
    if current_user.role == 'Developer':
        # Developer mendapatkan daftar semua sekolah
        all_schools = School.query.order_by(School.name).all()
        school_list = [s.to_dict() for s in all_schools]
        
        # Juga kirim semua mata pelajaran sekali jalan
        subjects = Subject.query.order_by(Subject.name).all()
        subject_list = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        
        return jsonify({
            'is_developer': True,
            'all_schools': school_list,
            'subjects': subject_list 
        }), 200

    elif current_user.role == 'School Admin':
        if not current_user.school_id:
            return jsonify({"message": "Admin tidak terikat dengan sekolah manapun"}), 404
        
        school = School.query.get(current_user.school_id)
        if not school:
            return jsonify({"message": "Sekolah tidak ditemukan"}), 404

        teachers = school.teachers 
        teacher_list = [{'id': teacher.id, 'name': teacher.username} for teacher in teachers]

        subjects = Subject.query.order_by(Subject.name).all()
        subject_list = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        
        grade_levels = []
        if school.level == 'SD/MI': grade_levels = list(range(1, 7))
        elif school.level == 'SMP/MTs': grade_levels = list(range(7, 10))
        elif school.level == 'SMA/MA': grade_levels = list(range(10, 13))

        return jsonify({
            'is_developer': False,
            'school': school.to_dict(),
            'teachers': teacher_list,
            'subjects': subject_list,
            'grade_levels': grade_levels
        }), 200
        
    else:
        return jsonify({"message": "Akses ditolak"}), 403

@class_bp.route('/api/schools/<int:school_id>/details-for-class', methods=['GET'])
@token_required
def get_school_details(current_user, school_id):
    """Mengambil detail (guru, tingkat kelas) dari sekolah tertentu."""
    if current_user.role != 'Developer':
        return jsonify({"message": "Akses hanya untuk Developer"}), 403

    school = School.query.get_or_404(school_id)

    teachers = school.teachers
    teacher_list = [{'id': teacher.id, 'name': teacher.username} for teacher in teachers]

    grade_levels = []
    if school.level == 'SD/MI': grade_levels = list(range(1, 7))
    elif school.level == 'SMP/MTs': grade_levels = list(range(7, 10))
    elif school.level == 'SMA/MA': grade_levels = list(range(10, 13))
    
    # Ambil juga daftar kelas yang sudah ada di sekolah ini
    existing_classes = Class.query.filter_by(school_id=school_id).all()

    return jsonify({
        'teachers': teacher_list,
        'grade_levels': grade_levels,
        'classes': [c.to_dict() for c in existing_classes]
    }), 200

@class_bp.route('/api/classes', methods=['GET'])
@token_required
def get_classes(current_user):
    """Mengambil semua kelas berdasarkan sekolah dari admin yang login."""
    
    # Developer bisa melihat semua kelas (opsional, bisa dihapus jika tidak perlu)
    if current_user.role == 'Developer':
        classes = Class.query.all()
    # Admin Sekolah hanya melihat kelas di sekolahnya
    elif current_user.role == 'School Admin' and current_user.school_id:
        classes = Class.query.filter_by(school_id=current_user.school_id).all()
    else:
        # Jika bukan admin atau admin tidak punya sekolah, kembalikan daftar kosong
        classes = []

    return jsonify([c.to_dict() for c in classes]), 200


# Endpoint [MODIFIKASI] untuk membuat kelas baru
@class_bp.route('/api/classes', methods=['POST'])
@token_required
def create_class(current_user):
    """Membuat kelas baru dengan struktur data yang lengkap."""
    if current_user.role != 'School Admin':
        return jsonify({"message": "Hanya Admin Sekolah yang bisa membuat kelas"}), 403

    data = request.get_json()
    required_fields = ['subject_id', 'teacher_id', 'grade_level', 'parallel_class']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Data tidak lengkap. Dibutuhkan subject, teacher, grade, dan parallel class.'}), 400

    new_class = Class(
        school_id=current_user.school_id,
        subject_id=data['subject_id'],
        teacher_id=data['teacher_id'],
        grade_level=data['grade_level'],
        parallel_class=str(data['parallel_class']).upper()
    )
    
    db.session.add(new_class)
    db.session.commit()
    
    # Mengambil data relasi agar bisa dikirim balik ke frontend
    created_class = Class.query.get(new_class.id)
    
    return jsonify(created_class.to_dict()), 201


# Endpoint [MODIFIKASI] untuk menghapus kelas
@class_bp.route('/api/classes/<int:class_id>', methods=['DELETE'])
@token_required
def delete_class(current_user, class_id):
    """Menghapus kelas berdasarkan ID."""
    cls = Class.query.get_or_404(class_id)
    
    # Otorisasi: Pastikan user yang menghapus adalah admin dari sekolah yang bersangkutan
    if current_user.role != 'Developer' and current_user.school_id != cls.school_id:
        return jsonify({"message": "Akses ditolak"}), 403
        
    db.session.delete(cls)
    db.session.commit()
    
    # Mengembalikan ID yang dihapus agar frontend tahu item mana yang harus dihapus dari state
    return jsonify({'message': 'Kelas berhasil dihapus', 'id': class_id}), 200

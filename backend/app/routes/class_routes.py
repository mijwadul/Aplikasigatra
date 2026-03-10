# backend/app/routes/class_routes.py

from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import School, Subject, User, Class
from app.utils.decorators import token_required

# Nama blueprint Anda adalah 'class_bp', kita akan tetap menggunakannya
class_bp = Blueprint('class_bp', __name__)

def _get_subjects_for_level(school_level):
    """
    Mengembalikan mata pelajaran yang cocok untuk jenjang sekolah.
    Termasuk: mata pelajaran dengan school_level yang sama + custom (school_level=None).
    """
    from sqlalchemy import or_
    subjects = Subject.query.filter(
        or_(Subject.school_level == school_level, Subject.school_level.is_(None))
    ).order_by(Subject.name).all()
    return [{'id': s.id, 'name': s.name} for s in subjects]


@class_bp.route('/api/classes/form-data', methods=['GET'])
@token_required
def get_form_data(current_user):
    """
    Mengirimkan data untuk form.
    - Untuk Admin, data sekolahnya otomatis + mata pelajaran sesuai jenjang sekolah.
    - Untuk Developer, daftar sekolah; mata pelajaran diambil setelah pilih sekolah.
    """
    if current_user.role == 'Developer':
        all_schools = School.query.order_by(School.name).all()
        school_list = [s.to_dict() for s in all_schools]
        return jsonify({
            'is_developer': True,
            'all_schools': school_list,
            'subjects': []  # Diisi setelah developer memilih sekolah
        }), 200

    elif current_user.role == 'School Admin':
        if not current_user.school_id:
            return jsonify({"message": "Admin tidak terikat dengan sekolah manapun"}), 404

        school = School.query.get(current_user.school_id)
        if not school:
            return jsonify({"message": "Sekolah tidak ditemukan"}), 404

        teachers = school.teachers
        teacher_list = [{'id': teacher.id, 'name': teacher.username} for teacher in teachers]
        subject_list = _get_subjects_for_level(school.level)

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
    """Mengambil detail (guru, mata pelajaran, tingkat kelas) dari sekolah tertentu."""
    if current_user.role != 'Developer':
        return jsonify({"message": "Akses hanya untuk Developer"}), 403

    school = School.query.get_or_404(school_id)

    teachers = school.teachers
    teacher_list = [{'id': teacher.id, 'name': teacher.username} for teacher in teachers]
    subject_list = _get_subjects_for_level(school.level)

    grade_levels = []
    if school.level == 'SD/MI': grade_levels = list(range(1, 7))
    elif school.level == 'SMP/MTs': grade_levels = list(range(7, 10))
    elif school.level == 'SMA/MA': grade_levels = list(range(10, 13))

    existing_classes = Class.query.filter_by(school_id=school_id).all()

    return jsonify({
        'teachers': teacher_list,
        'subjects': subject_list,
        'grade_levels': grade_levels,
        'classes': [c.to_dict() for c in existing_classes]
    }), 200

@class_bp.route('/api/classes', methods=['GET'])
@token_required
def get_classes(current_user):
    if current_user.role == 'Developer':
        classes = Class.query.all()

    elif current_user.role == 'School Admin' and current_user.school_id:
        classes = Class.query.filter_by(school_id=current_user.school_id).all()

    elif current_user.role == 'Teacher':
        teacher_schools = current_user.schools_taught
        school_ids = [s.id for s in teacher_schools]
        classes = Class.query.filter(Class.school_id.in_(school_ids)).all()

    else:
        classes = []

    return jsonify([c.to_dict() for c in classes]), 200



# Endpoint [MODIFIKASI] untuk membuat kelas baru
@class_bp.route('/api/classes', methods=['POST'])
@token_required
def create_class(current_user):
    """
    Membuat kelas baru — mendukung School Admin dan Developer.
    - School Admin: school_id dari current_user
    - Developer: wajib mengirim school_id di request body
    """
    if current_user.role not in ['School Admin', 'Developer']:
        return jsonify({"message": "Akses ditolak"}), 403

    data = request.get_json()
    required_fields = ['subject_id', 'teacher_id', 'grade_level', 'parallel_class']
    if current_user.role == 'Developer':
        required_fields.append('school_id')

    # Cek kelengkapan data
    if not all(field in data for field in required_fields):
        return jsonify({'message': f'Data tidak lengkap. Dibutuhkan: {", ".join(required_fields)}'}), 400

    # Tentukan school_id
    school_id = current_user.school_id if current_user.role == 'School Admin' else data.get('school_id')

    # Validasi school_id untuk Developer
    if current_user.role == 'Developer':
        school = School.query.get(school_id)
        if not school:
            return jsonify({"message": "School ID tidak valid"}), 404

    new_class = Class(
        school_id=school_id,
        subject_id=data['subject_id'],
        teacher_id=data['teacher_id'],
        grade_level=data['grade_level'],
        parallel_class=str(data['parallel_class']).upper()
    )

    db.session.add(new_class)
    db.session.commit()

    created_class = Class.query.get(new_class.id)
    return jsonify(created_class.to_dict()), 201


@class_bp.route('/api/classes/<int:class_id>', methods=['PUT'])
@token_required
def update_class(current_user, class_id):
    """Mengubah data kelas yang sudah ada."""
    if current_user.role not in ['School Admin', 'Developer']:
        return jsonify({"message": "Akses ditolak"}), 403

    cls = Class.query.get_or_404(class_id)
    if current_user.role != 'Developer' and current_user.school_id != cls.school_id:
        return jsonify({"message": "Akses ditolak"}), 403

    data = request.get_json()
    required_fields = ['subject_id', 'teacher_id', 'grade_level', 'parallel_class']
    if current_user.role == 'Developer':
        required_fields.append('school_id')

    if not all(field in data for field in required_fields):
        return jsonify({'message': f'Data tidak lengkap. Dibutuhkan: {", ".join(required_fields)}'}), 400

    if current_user.role == 'School Admin':
        school_id = current_user.school_id
    else:
        school_id = data.get('school_id')
        school = School.query.get(school_id) if school_id else None
        if not school:
            return jsonify({"message": "School ID tidak valid"}), 404

    cls.school_id = school_id
    cls.subject_id = data['subject_id']
    cls.teacher_id = data['teacher_id']
    cls.grade_level = data['grade_level']
    cls.parallel_class = str(data['parallel_class']).upper()

    db.session.commit()
    return jsonify(cls.to_dict()), 200


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

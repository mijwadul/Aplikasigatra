from flask import Blueprint, jsonify
from app.models import GeneratedDocument, Class, School
from app.utils.decorators import token_required

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    """Returns document count, class count, and school count for the current user."""
    docs_count = GeneratedDocument.query.filter_by(created_by_id=current_user.id).count()

    if current_user.role == 'Developer':
        classes_count = Class.query.count()
        schools_count = School.query.count()
    elif current_user.role == 'School Admin':
        classes_count = Class.query.filter_by(school_id=current_user.school_id).count()
        schools_count = 1 if current_user.school_id else 0
    else:
        # Teacher
        classes_count = Class.query.filter_by(teacher_id=current_user.id).count()
        schools_count = len(current_user.schools_taught) if current_user.schools_taught else 0

    recent_docs = (
        GeneratedDocument.query.filter_by(created_by_id=current_user.id)
        .order_by(GeneratedDocument.created_at.desc())
        .limit(5)
        .all()
    )
    recent_activity = [
        {
            'title': doc.title,
            'document_type': doc.document_type,
            'created_at': doc.created_at.isoformat() if doc.created_at else None,
        }
        for doc in recent_docs
    ]

    return jsonify({
        'documents_count': docs_count,
        'classes_count': classes_count,
        'schools_count': schools_count,
        'recent_activity': recent_activity,
    })

"""
Routes untuk mengelola cache hasil pencarian internet
"""
from flask import Blueprint, request, jsonify
from app.services.cache_service import get_cache_stats, clear_old_cache, clear_all_cache
from app.utils.decorators import token_required

cache_bp = Blueprint('cache_bp', __name__)

@cache_bp.route('/api/cache/stats', methods=['GET'])
@token_required
def get_cache_statistics(current_user):
    """
    Mendapatkan statistik cache (hanya untuk admin dan developer)
    """
    if current_user.role not in ['Admin', 'Developer']:
        return jsonify({"error": "Access denied. Only Admin and Developer can access cache statistics."}), 403
    
    stats = get_cache_stats()
    return jsonify(stats), 200

@cache_bp.route('/api/cache/clear-old', methods=['POST'])
@token_required
def clear_cache_old(current_user):
    """
    Menghapus cache yang lebih lama dari hari yang ditentukan (hanya untuk admin dan developer)
    """
    if current_user.role not in ['Admin', 'Developer']:
        return jsonify({"error": "Access denied. Only Admin and Developer can clear cache."}), 403
    
    data = request.get_json() or {}
    days_old = data.get('days_old', 7)  # Default 7 hari
    
    result = clear_old_cache(days_old)
    return jsonify(result), 200

@cache_bp.route('/api/cache/clear-all', methods=['POST'])
@token_required
def clear_cache_all(current_user):
    """
    Menghapus SEMUA cache (hanya untuk developer)
    """
    if current_user.role != 'Developer':
        return jsonify({"error": "Access denied. Only Developer can clear all cache."}), 403
    
    result = clear_all_cache()
    return jsonify(result), 200

@cache_bp.route('/api/cache/search', methods=['POST'])
@token_required
def search_cache_only(current_user):
    """
    Mencari HANYA di cache, tidak di dokumen asli (hanya untuk admin dan developer)
    """
    if current_user.role not in ['Admin', 'Developer']:
        return jsonify({"error": "Access denied. Only Admin and Developer can search cache."}), 403
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required."}), 400
    
    from app.services.cache_service import search_cache_only
    results = search_cache_only(data['query'])
    
    if results:
        return jsonify({"results": results, "found": True}), 200
    else:
        return jsonify({"results": [], "found": False, "message": "No cache results found for the query."}), 200

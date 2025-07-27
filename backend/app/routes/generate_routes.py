from flask import Blueprint, request, jsonify
from app.services.rag_service import search_index
from app.services.ai_service import generate_content_with_context

generate_bp = Blueprint('generate_bp', __name__)

@generate_bp.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required."}), 400

    query = data['query']

    # 1. Retrieve relevant context from our RAG index
    context_chunks = search_index(query)

    if not context_chunks:
        return jsonify({"error": "Could not find relevant context in the uploaded documents."}), 404

    # 2. Generate content using the AI with the retrieved context
    generated_content = generate_content_with_context(query, context_chunks)

    return jsonify({"content": generated_content}), 200
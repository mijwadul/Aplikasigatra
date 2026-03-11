"""
Cache Service untuk mengelola hasil pencarian internet yang disimpan di ChromaDB
"""
import chromadb
import os
from datetime import datetime, timedelta
from .rag_service import collection

def get_cache_stats():
    """
    Mengembalikan statistik cache yang tersimpan di ChromaDB
    """
    try:
        # Ambil semua data dari collection
        all_data = collection.get()
        
        if not all_data['ids']:
            return {
                'total_cached_items': 0,
                'cache_items': []
            }
        
        # Filter hanya cache items (dimulai dengan 'internet_search_')
        cache_items = []
        for i, doc_id in enumerate(all_data['ids']):
            if doc_id.startswith('internet_search_'):
                document = all_data['documents'][i] if i < len(all_data['documents']) else ""
                # Extract key dari document ID
                cache_key = doc_id.replace('internet_search_', '')
                
                # Parse timestamp jika ada
                created_time = "Unknown"
                if "CREATED_AT:" in document:
                    try:
                        time_str = document.split("CREATED_AT:")[1].split("\n")[0].strip()
                        created_time = time_str
                    except:
                        pass
                
                cache_items.append({
                    'cache_key': cache_key,
                    'document_id': doc_id,
                    'created_at': created_time,
                    'preview': document[:100] + "..." if len(document) > 100 else document
                })
        
        return {
            'total_cached_items': len(cache_items),
            'cache_items': cache_items
        }
        
    except Exception as e:
        print(f"Error getting cache stats: {e}")
        return {
            'total_cached_items': 0,
            'cache_items': [],
            'error': str(e)
        }

def clear_old_cache(days_old=7):
    """
    Menghapus cache yang lebih lama dari hari yang ditentukan
    """
    try:
        # Ambil semua data
        all_data = collection.get()
        
        if not all_data['ids']:
            return {'deleted_count': 0, 'message': 'No cache items found'}
        
        # Identifikasi cache items yang akan dihapus
        ids_to_delete = []
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for i, doc_id in enumerate(all_data['ids']):
            if doc_id.startswith('internet_search_'):
                document = all_data['documents'][i] if i < len(all_data['documents']) else ""
                
                # Cek timestamp
                should_delete = True  # Default delete jika tidak ada timestamp
                if "CREATED_AT:" in document:
                    try:
                        time_str = document.split("CREATED_AT:")[1].split("\n")[0].strip()
                        created_date = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                        should_delete = created_date < cutoff_date
                    except:
                        pass
                
                if should_delete:
                    ids_to_delete.append(doc_id)
        
        # Hapus items
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
            return {
                'deleted_count': len(ids_to_delete),
                'message': f'Successfully deleted {len(ids_to_delete)} old cache items'
            }
        else:
            return {
                'deleted_count': 0,
                'message': f'No cache items older than {days_old} days found'
            }
            
    except Exception as e:
        print(f"Error clearing old cache: {e}")
        return {
            'deleted_count': 0,
            'error': str(e)
        }

def clear_all_cache():
    """
    Menghapus SEMUA cache items (hanya cache, bukan dokumen asli)
    """
    try:
        all_data = collection.get()
        
        if not all_data['ids']:
            return {'deleted_count': 0, 'message': 'No items found'}
        
        # Hanya hapus cache items
        cache_ids = [doc_id for doc_id in all_data['ids'] if doc_id.startswith('internet_search_')]
        
        if cache_ids:
            collection.delete(ids=cache_ids)
            return {
                'deleted_count': len(cache_ids),
                'message': f'Successfully deleted all {len(cache_ids)} cache items'
            }
        else:
            return {
                'deleted_count': 0,
                'message': 'No cache items found'
            }
            
    except Exception as e:
        print(f"Error clearing all cache: {e}")
        return {
            'deleted_count': 0,
            'error': str(e)
        }

def search_cache_only(query):
    """
    Mencari HANYA di cache, tidak di dokumen asli
    """
    try:
        # Tambahkan prefix untuk memastikan hanya cache yang dicari
        cache_query = f"internet_search_{query}"
        results = collection.query(
            query_texts=[cache_query],
            n_results=5
        )
        
        if results['documents'] and results['documents'][0]:
            # Filter hasil untuk memastikan hanya cache yang dikembalikan
            cache_results = []
            for doc in results['documents'][0]:
                if "INTERNET_SEARCH_CACHE_" in doc:
                    # Extract actual content dari cache
                    content = doc.split("INTERNET_SEARCH_CACHE_")[1].split(": ", 1)[1]
                    cache_results.append(content)
            
            return cache_results if cache_results else None
        
        return None
        
    except Exception as e:
        print(f"Error searching cache: {e}")
        return None

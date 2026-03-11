import sqlite3
import os

# Path ke database
db_path = os.path.join(os.path.dirname(__file__), 'gatra_sinau.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cek struktur tabel generated_document
    print("=== STRUKTUR TABEL GENERATED_DOCUMENT ===")
    cursor.execute("PRAGMA table_info(generated_document)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"Column: {col[1]} | Type: {col[2]} | NotNull: {col[3]}")
    
    print("\n=== DATA DI TABEL GENERATED_DOCUMENT ===")
    # Cek semua data
    cursor.execute("SELECT id, title, created_by_id, created_at FROM generated_document ORDER BY created_at DESC")
    docs = cursor.fetchall()
    
    if docs:
        print(f"Total dokumen: {len(docs)}")
        for doc in docs:
            print(f"ID: {doc[0]} | Title: {doc[1]} | User ID: {doc[2]} | Created: {doc[3]}")
    else:
        print("Tidak ada dokumen di database")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")

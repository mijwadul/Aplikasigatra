import os
import google.generativeai as genai

# Configure the library with the API key from the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_content_with_context(query, context_chunks):
    """Generates content using the Gemini model with provided context."""
    print("Generating AI content with Gemini...")
    
    # Combine the context chunks into a single string
    context = "\n\n---\n\n".join(context_chunks)
    
    # Construct a single, detailed prompt for the Gemini model
    full_prompt = (
        "Anda adalah asisten ahli untuk guru Indonesia, yang selaras dengan Kurikulum Merdeka. "
        "Gunakan konteks yang disediakan dari dokumen kurikulum resmi untuk menjawab permintaan pengguna secara akurat. "
        "Hasilkan tanggapan dalam Bahasa Indonesia.\n\n"
        f"Konteks:\n{context}\n\n"
        f"Permintaan Pengguna: '{query}'"
    )

    try:
        response = model.generate_content(full_prompt)
        ai_response = response.text
        print("AI content generated successfully.")
        return ai_response
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        return "Maaf, terjadi kesalahan saat menghubungi layanan AI Gemini."
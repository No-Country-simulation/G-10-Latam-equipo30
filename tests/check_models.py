import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: No se encontró GEMINI_API_KEY en el archivo .env")
        return
        
    genai.configure(api_key=api_key)
    
    print("Conectando con Google AI...")
    print("Modelos de Embeddings disponibles para tu API Key:\n")
    
    try:
        encontrados = False
        for m in genai.list_models():
            if 'embedContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                encontrados = True
                
        if not encontrados:
            print("❌ Tu API Key no tiene acceso a ningún modelo de embeddings.")
            
    except Exception as e:
        print(f"Error al conectar con la API: {e}")

if __name__ == "__main__":
    main()

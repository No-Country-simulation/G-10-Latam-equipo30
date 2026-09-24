from ingestion import process_document
from ChunkEmbeddings import chunk_embeddings

if __name__ == "__main__":
    # Ruta relativa considerando que ejecutamos desde la raíz del proyecto
    sample_file = "data/documento_prueba.md"

    try:
        docs = process_document(sample_file)
        print(f"Éxito: Se procesaron {len(docs)} páginas/fragmentos.")
        if docs:
            print("\n--- Muestra del texto limpio ---")
            print(docs[0].page_content[:300])
            print("\n--- Fin de la muestra ---")
            chunk_embeddings(docs)
    except (OSError, ValueError) as e:
        print(f"Error de ejecución: {e}")

import os
import sys
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(base_dir, "../src")))

from chunk_embeddings import chunk_embeddings
from ingestion import process_document


def main():
    # Resolver la ruta absoluta de la carpeta data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "../data")

    # Buscar todos los archivos soportados
    files_to_process = []
    for ext in ("*.md", "*.pdf", "*.txt"):
        files_to_process.extend(glob.glob(os.path.join(data_dir, ext)))

    if not files_to_process:
        print(f"Error: No se encontraron archivos de prueba en {data_dir}")
        return

    print(
        f"Archivos encontrados a procesar: {[os.path.basename(f) for f in files_to_process]}\n"
    )

    all_docs = []
    print("1. Iniciando ingesta de documentos...")
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        try:
            docs = process_document(file_path)
            print(
                f"   - {filename}: se extrajeron {len(docs)} fragmentos/páginas base."
            )
            all_docs.extend(docs)
        except Exception as e:
            print(f"   - Error procesando {filename}: {e}")

    if not all_docs:
        print("Error: No se pudo extraer texto de ningún archivo.")
        return

    print(
        f"\n2. Generando Chunks y Embeddings ({len(all_docs)} elementos base totales), y guardando en FAISS..."
    )
    try:
        chunk_embeddings(all_docs)
        print("\n   ¡Éxito! El VectorStore se ha guardado en la carpeta 'vectorstore'.")
        print("   La Fase 2 está funcionando correctamente en lote.")
    except Exception as e:
        print(f"\nError durante los Embeddings: {e}")


if __name__ == "__main__":
    main()

import sys
from pathlib import Path

from chunk_embeddings import chunk_embeddings
from ingestion import process_document

# Formatos soportados por la ingesta (F01).
EXTENSIONES = {".pdf", ".md", ".txt"}
CARPETA_DATOS = Path("data")


def buscar_archivos(argumentos):
    """Usa los archivos pasados por consola o, si no hay, todos los de data/."""
    if argumentos:
        return [Path(a) for a in argumentos]
    if not CARPETA_DATOS.is_dir():
        return []
    return sorted(p for p in CARPETA_DATOS.iterdir() if p.suffix.lower() in EXTENSIONES)


if __name__ == "__main__":
    # Ejecutar desde la raíz del proyecto:
    #   python src/main.py                 -> procesa todo data/
    #   python src/main.py data/archivo.md -> procesa solo ese archivo
    archivos = buscar_archivos(sys.argv[1:])
    if not archivos:
        print("No se encontraron archivos .pdf, .md o .txt para procesar.")
        sys.exit(1)

    docs = []
    for archivo in archivos:
        try:
            docs_archivo = process_document(str(archivo))
            print(f"{archivo.name}: {len(docs_archivo)} páginas/fragmentos.")
            docs.extend(docs_archivo)
        except (OSError, ValueError) as e:
            print(f"Error procesando {archivo.name}: {e}")

    if not docs:
        print("No se pudo extraer texto de ningún archivo.")
        sys.exit(1)

    print("\n--- Muestra del texto limpio ---")
    print(docs[0].page_content[:300])
    print("--- Fin de la muestra ---\n")

    chunk_embeddings(docs)
    print("Índice guardado en la carpeta 'vectorstore'.")

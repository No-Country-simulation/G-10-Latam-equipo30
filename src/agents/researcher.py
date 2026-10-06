import os
import sys

# Agregamos la carpeta src al path para poder importar los módulos locales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from state import AgentState

def get_retriever():
    """Inicializa y devuelve el retriever apuntando a nuestra base vectorial local."""
    from chunk_embeddings import cargar_vectorstore
    
    # Cargamos la base de datos vectorial generada en la Fase 2
    vectorstore = cargar_vectorstore()

    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 4},
    )


def researcher_node(state: AgentState) -> dict:
    """Nodo responsable de recuperar contexto del Vector Store según la consulta."""
    print("🔍 [Agente Investigador] Buscando contexto en la base de conocimientos...")

    query = state["query"]
    retriever = get_retriever()
    documents = retriever.invoke(query)

    print(
        f"📚 [Agente Investigador] Se encontraron {len(documents)} fragmentos relevantes para '{query}'."
    )

    # Devolvemos la actualización del estado
    return {
        "retrieved_docs": documents,
        "revision_attempts": 0,  # Inicializamos el contador para el ciclo de revisión
    }

import typer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from machine_learning.embedding_model import TextEmbedder
from machine_learning.search import FaissIndexer
from ingest_data.ingest_notion import get_notion_pages

notion_docs = get_notion_pages()
title_index = None
paragraph_index = None 
embedder = None  # Initialize the embedder at the module level

app = typer.Typer()

# Event to initialize the text embedder
@app.callback()
def load_embedder():
    global embedder
    embedder = TextEmbedder()


def populate_index():
    global title_index, paragraph_index, notion_docs
    # Populate the indexes with notion documents if necessary.
    if not notion_docs:
        notion_docs = get_notion_pages()
        
    for page in notion_docs:
        page.title.embedding = embedder.embed(page.title.content)
        for paragraph in page.blocks: 
            paragraph.embedding = embedder.embed(paragraph.text_content)

    for doc in notion_docs: 
        doc.indexed = True

def search_index(query: str):
    global notion_docs, embedder

    if not any([doc.indexed for doc in notion_docs]) or embedder is None:
        raise ValueError("Index not populated. Run populate_index first.")

    query_embedding = embedder.embed(query)
    title_embeddings = [title_element.title.embedding for title_element in notion_docs]
    title_similarities = cosine_similarity(query_embedding.reshape(1, -1), title_embeddings)
    
    # Get indices that would sort the similarities in descending order
    sorted_indices = np.argsort(title_similarities[0])[::-1]

    # Sort notion_docs based on sorted_indices
    sorted_docs = [notion_docs[idx] for idx in sorted_indices]
    
    for i, doc in enumerate(sorted_docs):
        print("Similarity:", title_similarities[0][i])
        print("Title:", doc.title.content)
        print("=" * 50)

@app.command()
def search_notion(query: str, rebuild: bool = typer.Option(False, "--rebuild")):
    global notion_docs, title_index, paragraph_index

    if rebuild:
        notion_docs = get_notion_pages()
    populate_index()
    search_index(query=query)
    """# Embed the query using the text embedder.
    query_embedding = embedder.embed(query)

    # Search the title index and retrieve the most relevant title IDs.
    top_k_title_ids = search_index(title_index, query_embedding, top_k=3)

    # Search the paragraph index and retrieve the most relevant paragraph IDs.
    top_k_paragraph_ids = search_index(paragraph_index, query_embedding, top_k=3)

    # Print relevant titles and paragraphs
    print("Relevant Titles:")
    for title_id in top_k_title_ids[0]:
        relevant_title = notion_docs[title_id]
        print(relevant_title["title"])
        print("=" * 50)

    print("Relevant Paragraphs:")
    for paragraph_id in top_k_paragraph_ids[0]:
        relevant_paragraph = notion_docs[paragraph_id]
        print(relevant_paragraph["text_content"])
        print("=" * 50)"""

if __name__ == "__main__":
    app()

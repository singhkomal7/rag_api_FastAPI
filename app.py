from fastapi import FastAPI

import chromadb
import ollama

app = FastAPI()
chroma = chromadb.PersistentClient(path='./db')
collection = chroma.get_or_create_collection('docs')

@app.post('/query')
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results['documents'][0][0] if results['documents'] else ""

    answer = ollama.generate(
        model = 'tinyllama',
        prompt=f'Conext:\n{context}\n\nQuestion: {q}\n\nAnswer clear and conciselt:'
    )

    return {'answer': answer['response']}

@app.post('/add')
def add_knowledge(text: str):\

    try: 

        import uuid
        docs_id = str(uuid.uuid4())

        collection.add(documents=[text], ids=[doc_id])

        return {
            "status": "success",
            "message": "Contents added to knowledge base",
            "id": docs_id
        }
    except Exception as e:
        
        return {
            "status": "error",
            "message": str(e)
        }

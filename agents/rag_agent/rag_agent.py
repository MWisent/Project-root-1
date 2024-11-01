# agents/rag_agent/agent.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging

class Document(BaseModel):
    """Model dokumentu"""
    id: str
    content: str
    metadata: Optional[Dict] = None
    embedding: Optional[List[float]] = None

class RAGAgent:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents: Dict[str, Document] = {}
        self.embeddings: Dict[str, np.ndarray] = {}
        
    async def add_document(self, doc: Document) -> bool:
        """Dodawanie dokumentu do bazy"""
        try:
            # Generowanie embeddingu
            embedding = self.encoder.encode(doc.content)
            
            # Zapisywanie dokumentu i embeddingu
            self.documents[doc.id] = doc
            self.embeddings[doc.id] = embedding
            
            return True
        except Exception as e:
            logging.error(f"Error adding document: {str(e)}")
            return False
    
    async def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Wyszukiwanie dokumentów"""
        try:
            query_embedding = self.encoder.encode(query)
            
            # Obliczanie podobieństwa
            similarities = {}
            for doc_id, doc_embedding in self.embeddings.items():
                similarity = np.dot(query_embedding, doc_embedding)
                similarities[doc_id] = similarity
            
            # Sortowanie wyników
            top_docs = sorted(
                similarities.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:top_k]
            
            return [
                {
                    "document": self.documents[doc_id].dict(),
                    "score": float(score)
                }
                for doc_id, score in top_docs
            ]
        except Exception as e:
            logging.error(f"Error during search: {str(e)}")
            return []
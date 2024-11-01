# tests/test_rag_agent.py
import pytest
from agents.rag_agent.agent import RAGAgent, Document

@pytest.fixture
def rag_agent():
    return RAGAgent()

@pytest.fixture
def sample_documents():
    return [
        Document(
            id="doc1",
            content="Python is a programming language"
        ),
        Document(
            id="doc2",
            content="JavaScript is used for web development"
        )
    ]

@pytest.mark.asyncio
async def test_document_addition(rag_agent, sample_documents):
    for doc in sample_documents:
        success = await rag_agent.add_document(doc)
        assert success
    assert len(rag_agent.documents) == 2

@pytest.mark.asyncio
async def test_document_search(rag_agent, sample_documents):
    # Add documents
    for doc in sample_documents:
        await rag_agent.add_document(doc)
    
    # Search
    results = await rag_agent.search("Python programming")
    assert len(results) > 0
    assert results[0]["document"]["id"] == "doc1"
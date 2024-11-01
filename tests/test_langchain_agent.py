# tests/test_langchain_agent.py
import pytest
from agents.langchain_agent.langchan_agent import LangChainAgent, AgentConfig

@pytest.mark.asyncio
async def test_langchain_agent_initialization():
    config = AgentConfig()
    agent = LangChainAgent(config)
    assert agent.config == config
    assert agent.tools is not None
    assert len(agent.tools) == 2

@pytest.mark.asyncio
async def test_langchain_agent_query_processing():
    config = AgentConfig()
    agent = LangChainAgent(config)
    response = await agent.process_query(
        "What is the capital of France?"
    )
    assert response["status"] == "success"
    assert response["error"] is None
    assert "Paris" in response["response"].lower()

@pytest.mark.asyncio
async def test_langchain_agent_error_handling():
    config = AgentConfig(model_name="invalid_model")
    agent = LangChainAgent(config)
    response = await agent.process_query("Test query")
    assert response["status"] == "error"
    assert response["error"] is not None
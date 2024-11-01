# agents/langchain_agent/agent.py
from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

class AgentConfig(BaseModel):
    """Konfiguracja agenta"""
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 500
    tools: List[str] = ["search", "calculator"]

class LangChainAgent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = OpenAI(
            temperature=config.temperature,
            model_name=config.model_name
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()
        
    def _initialize_tools(self) -> List[Tool]:
        """Inicjalizacja narzędzi agenta"""
        tools = []
        if "search" in self.config.tools:
            tools.append(Tool(
                name="Search",
                func=self._search_tool,
                description="Useful for searching information"
            ))
        if "calculator" in self.config.tools:
            tools.append(Tool(
                name="Calculator",
                func=self._calculator_tool,
                description="Useful for mathematical calculations"
            ))
        return tools
    
    def _initialize_agent(self):
        """Inicjalizacja agenta"""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent="chat-conversational-react-description",
            memory=self.memory,
            verbose=True
        )
    
    async def process_query(self, query: str) -> Dict:
        """Przetwarzanie zapytania"""
        try:
            response = await self.agent.arun(query)
            return {
                "status": "success",
                "response": response,
                "error": None
            }
        except Exception as e:
            logging.error(f"Error processing query: {str(e)}")
            return {
                "status": "error",
                "response": None,
                "error": str(e)
            }
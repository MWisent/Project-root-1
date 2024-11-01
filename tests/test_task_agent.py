# tests/test_task_agent.py
import pytest
from agents.task_agent.agent import TaskAgent
from datetime import datetime, timedelta

@pytest.fixture
def task_agent():
    return TaskAgent()

@pytest.fixture
def sample_task_data():
    return {
        "title": "Test Task",
        "description": "Test Description",
        "assignee": "test@example.com",
        "due_date": datetime.now() + timedelta(days=1),
        "priority": "high"
    }

@pytest.mark.asyncio
async def test_task_creation(task_agent, sample_task_data):
    task = await task_agent.create_task(sample_task_data)
    assert task is not None
    assert task.title == sample_task_data["title"]
    assert task.priority == sample_task_data["priority"]

@pytest.mark.asyncio
async def test_task_update(task_agent, sample_task_data):
    task = await task_agent.create_task(sample_task_data)
    updated_task = await task_agent.update_task(
        task.id,
        {"status": "in_progress"}
    )
    assert updated_task is not None
    assert updated_task.status == "in_progress"

@pytest.mark.asyncio
async def test_task_filtering(task_agent, sample_task_data):
    await task_agent.create_task(sample_task_data)
    await task_agent.create_task({
        **sample_task_data,
        "priority": "low"
    })
    
    high_priority_tasks = await task_agent.get_tasks(
        {"priority": "high"}
    )
    assert len(high_priority_tasks) == 1
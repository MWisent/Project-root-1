# agents/task_agent/agent.py
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

class Task(BaseModel):
    """Model zadania"""
    id: str
    title: str
    description: Optional[str]
    status: str = "pending"
    assignee: Optional[str]
    due_date: Optional[datetime]
    priority: str = "medium"
    tags: List[str] = []

class TaskAgent:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        
    async def create_task(self, task_data: Dict) -> Optional[Task]:
        """Tworzenie nowego zadania"""
        try:
            task_id = f"task_{len(self.tasks) + 1}"
            task = Task(id=task_id, **task_data)
            self.tasks[task_id] = task
            return task
        except Exception as e:
            logging.error(f"Error creating task: {str(e)}")
            return None
    
    async def update_task(
        self, 
        task_id: str, 
        updates: Dict
    ) -> Optional[Task]:
        """Aktualizacja zadania"""
        try:
            if task_id not in self.tasks:
                return None
            
            current_task = self.tasks[task_id]
            updated_data = current_task.dict()
            updated_data.update(updates)
            
            updated_task = Task(**updated_data)
            self.tasks[task_id] = updated_task
            
            return updated_task
        except Exception as e:
            logging.error(f"Error updating task: {str(e)}")
            return None
    
    async def get_tasks(
        self, 
        filters: Optional[Dict] = None
    ) -> List[Task]:
        """Pobieranie zadań z opcjonalnymi filtrami"""
        try:
            if not filters:
                return list(self.tasks.values())
            
            filtered_tasks = []
            for task in self.tasks.values():
                matches = all(
                    getattr(task, key) == value 
                    for key, value in filters.items()
                )
                if matches:
                    filtered_tasks.append(task)
            
            return filtered_tasks
        except Exception as e:
            logging.error(f"Error getting tasks: {str(e)}")
            return []
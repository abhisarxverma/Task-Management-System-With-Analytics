from datetime import datetime, timedelta
import json
import os
import uuid
from enum import Enum
from typing import Dict, Optional

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task:
    def __init__(self, title: str, description: str, 
                 due_date: Optional[str] = None,
                 priority: Priority = Priority.MEDIUM, 
                 status: Status = Status.PENDING,
                 task_id: Optional[str] = None):
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_at = datetime.now().strftime("%Y-%m-%d")
        self.due_date = due_date or (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "due_date": self.due_date,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Task":
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data.get("due_date"),
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            task_id=data["task_id"]
        )

class TaskManager:
    FILE_PATH = "tasks.json"

    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self) -> Dict[str, Dict]:
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        return {}

    def save_tasks(self):
        with open(self.FILE_PATH, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task.to_dict()
        self.save_tasks()
        print("✅ Task added successfully!")

    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            print(f"✅ Task {task_id} deleted successfully!")
        else:
            print("❌ Task not found!")

    def update_task(self, task_id: str, **kwargs):
        if task_id in self.tasks:
            for key, value in kwargs.items():
                if key in self.tasks[task_id]:
                    self.tasks[task_id][key] = value
            self.save_tasks()
            print("✅ Task updated successfully!")
        else:
            print("❌ Task not found!")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        print(f"{'ID':<36} | {'Title':<20} | {'Status':<10} | {'Priority':<10} | {'Due Date'}")
        print("-" * 110)
        for task in self.tasks.values():
            print(f"{task['task_id']:<36} | {task['title']:<20} | {task['status']:<10} | {task['priority']:<10} | {task['due_date']}")


def main():
    task_manager = TaskManager()
    
    while True:
        print("\n1. List Tasks\n2. Add Task\n3. Update Task\n4. Delete Task\n5. Exit")
        print()
        choice = input("Enter choice: ")
        
        if choice == "1":
            task_manager.list_tasks()
        elif choice == "2":
            title = input("Title: ")
            description = input("Description: ")
            priority = input("Priority (high/medium/low): ").lower()
            task = Task(title, description, priority=Priority(priority))
            task_manager.add_task(task)
        elif choice == "3":
            task_id = input("Task ID: ")
            field = input("Field to update (title/description/status/priority/due_date): ")
            value = input(f"New value for {field}: ")
            task_manager.update_task(task_id, **{field: value})
        elif choice == "4":
            task_id = input("Task ID to delete: ")
            task_manager.delete_task(task_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
  

            

                


                



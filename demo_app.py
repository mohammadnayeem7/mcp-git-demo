"""
Demo app — a simple task manager used to simulate SDLC changes via git MCP.
"""


def add_task(tasks: list, title: str) -> list:
    task = {"id": len(tasks) + 1, "title": title, "done": False}
    tasks.append(task)
    return tasks


def complete_task(tasks: list, task_id: int) -> list:
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            break
    return tasks


def list_tasks(tasks: list) -> None:
    for task in tasks:
        status = "✓" if task["done"] else "○"
        print(f"  [{status}] #{task['id']} {task['title']}")


if __name__ == "__main__":
    tasks = []
    tasks = add_task(tasks, "Design feature")
    tasks = add_task(tasks, "Write code")
    tasks = add_task(tasks, "Write tests")
    tasks = complete_task(tasks, 1)
    print("Task list:")
    list_tasks(tasks)

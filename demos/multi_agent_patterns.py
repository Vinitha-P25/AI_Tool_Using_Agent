"""Small demos of sequential, supervisor-style, and hierarchical routing patterns.
These are architecture demonstrations, not autonomous production agents.
"""
from dataclasses import dataclass

@dataclass
class Task:
    kind: str
    text: str

def sequential(tasks):
    """Run deterministic stages in order."""
    result = ""
    for task in tasks:
        result = f"[{task.kind}] {task.text}" if not result else f"{result}\n -> [{task.kind}] {task.text}"
    return result

def supervisor(task: Task):
    """A supervisor routes a task to a specialist by task type."""
    routes = {
        "math": "calculator specialist",
        "research": "web research specialist",
        "api": "API specialist",
    }
    return routes.get(task.kind, "general assistant")

def hierarchical(task: Task):
    """A high-level planner splits a task into specialist sub-tasks."""
    if task.kind == "research_then_calculate":
        return [
            Task("research", "Find the relevant numeric facts"),
            Task("math", "Calculate using the verified facts"),
            Task("review", "Check the answer and summarize"),
        ]
    return [task]

if __name__ == "__main__":
    print("SEQUENTIAL:")
    print(sequential([
        Task("research", "Collect source information"),
        Task("analysis", "Analyze source information"),
        Task("review", "Check the final answer"),
    ]))
    print("\nSUPERVISOR ROUTING:")
    print(supervisor(Task("research", "Find recent Python release info")))
    print("\nHIERARCHICAL TASK BREAKDOWN:")
    for item in hierarchical(Task("research_then_calculate", "Research and calculate")):
        print(f"- {item.kind}: {item.text}")

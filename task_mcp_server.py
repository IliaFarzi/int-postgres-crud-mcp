from typing import Optional, Literal, List

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from domain.dto.create_task import CreateTask
from domain.dto.id_task import IdTask
from domain.dto.query_task import QueryTask
from domain.dto.update_task import UpdateTask
from domain.model.task import Task
from service.config_service import ConfigService
from service.task_service import TaskService


mcp = FastMCP("TaskManagement")

config = ConfigService(override=True).config
task_service = TaskService(url=str(config.db_url))

@mcp.tool()
def create_task(payload: CreateTask) -> Task:
    """
    Create a new task.

    Input:
      payload: CreateTask
        - title (str, required)
        - description (str, optional)
        - status (optional: 'pending' | 'in_progress' | 'done')

    Output:
      Task object with id, title, description, status, created_at, updated_at.

    Example call:
      {
        "payload": {
          "title": "Write documentation",
          "description": "Draft MCP server docs",
          "status": "pending"
        }
      }
    """
    try:
        return task_service.create_one(payload=payload)
    except ValueError as ve:
        raise ToolError(str(ve))
    except Exception:
        raise ToolError("internal_error: failed to create task")

@mcp.tool()
def list_tasks(query: Optional[QueryTask] = None) -> List[Task]:
    """
    List tasks with optional filters.

    Input:
      query (optional): QueryTask
        - title (str, optional, substring match)
        - description (str, optional, substring match)
        - status (optional: 'pending' | 'in_progress' | 'done')

    Output:
      List of Task objects. Returns an empty list if no tasks match.

    Example call (list all tasks):
      {}

    Example call (filtered):
      {
        "query": {
          "status": "pending",
          "title": "write"
        }
      }
    """
    try:
        return task_service.read_many(query=query or QueryTask())
    except Exception:
        raise ToolError("internal_error: failed to list tasks")

@mcp.tool()
def get_task_by_id(id: int) -> Task:
    """
    Retrieve a single task by ID.

    Input:
      id (int): Task identifier.

    Output:
      Task object.

    Errors:
      - not_found: task does not exist

    Example call:
      {
        "id": 42
      }
    """
    try:
        task = task_service.read_one(query=IdTask(id=id))
        if task is None:
            raise ToolError(f"not_found: task with id {id} does not exist")
        return task
    except ToolError:
        raise
    except Exception:
        raise ToolError("internal_error: failed to fetch task")

@mcp.tool()
def update_task_status(id: int, status: Literal["pending", "in_progress", "done"], ) -> Task:
    """
    Update the status of a task.

    Input:
      id (int): Task identifier.
      status (Literal): New status value.

    Output:
      Updated Task object.

    Errors:
      - not_found: task does not exist
      - validation_error: invalid status or update failure

    Example call:
      {
        "id": 42,
        "status": "done"
      }
    """
    try:
        updated = task_service.update_one(query=IdTask(id=id), payload=UpdateTask(status=status), )
        if updated is None:
            raise ToolError(f"not_found: task with id {id} does not exist")
        return updated
    except ValueError as ve:
        raise ToolError(f"validation_error: {ve}")
    except ToolError:
        raise
    except Exception:
        raise ToolError("internal_error: failed to update task")

@mcp.tool()
def delete_task(id: int) -> bool:
    """
    Delete a task by ID.

    Input:
      id (int): Task identifier.

    Output:
      true if deletion succeeded.

    Errors:
      - not_found: task does not exist

    Example call:
      {
        "id": 42
      }
    """
    try:
        deleted = task_service.delete_one(query=IdTask(id=id))
        if not deleted:
            raise ToolError(f"not_found: task with id {id} does not exist")
        return True
    except ToolError:
        raise
    except Exception:
        raise ToolError("internal_error: failed to delete task")


if __name__ == "__main__":
    mcp.run(transport="stdio")

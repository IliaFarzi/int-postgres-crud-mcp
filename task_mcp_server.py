from typing import Literal, List

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
    Creates a new task using the provided payload.
    Input: payload (CreateTask) with title, description, and optional status.
    Output: Task object representing the newly created task, including id, status, created_at, and updated_at.
    """
    try:
        return task_service.create_one(payload=payload)
    except ValueError as ve:
        raise ToolError(str(ve))
    except Exception as e:
        raise ToolError("Unexpected error while creating task")


@mcp.tool()
def list_tasks(query: QueryTask) -> List[Task]:
    """
    Retrieves a list of tasks filtered by optional query parameters.
    Input: query (QueryTask) with optional title, description, and status.
    Output: List of Task objects matching the filters; empty list if no tasks match.
    """
    try:
        return task_service.read_many(query=query)
    except Exception as e:
        raise ToolError("Unexpected error while listing tasks")


@mcp.tool()
def get_task_by_id(id: int) -> Task:
    """
    Retrieves a single task by its ID.
    Input: id (int) representing the task identifier.
    Output: Task object corresponding to the ID.
    Raises ToolError with code 'not_found' if the task does not exist.
    """
    try:
        task = task_service.read_one(query=IdTask(id=id))
        if task is None:
            raise ToolError(f"Task with ID {id} not found")
        return task
    except ToolError:
        raise
    except Exception as e:
        raise ToolError("Unexpected error while fetching task")


@mcp.tool()
def update_task_status(id: int, status: Literal['pending', 'in_progress', 'done']) -> Task:
    """
    Updates the status field of a task by its ID.
    Input: id (int) of the task, status (Literal) new status value.
    Output: Task object representing the updated task with new status and updated_at timestamp.
    Raises ToolError with code 'not_found' if the task does not exist.
    Raises ToolError with code 'validation_error' if the update payload is invalid.
    """
    try:
        updated = task_service.update_one(query=IdTask(id=id), payload=UpdateTask(status=status))
        if updated is None:
            raise ToolError(f"Task with ID {id} not found")
        return updated
    except ValueError as ve:
        raise ToolError(str(ve))
    except ToolError:
        raise
    except Exception as e:
        raise ToolError("Unexpected error while updating task")


@mcp.tool()
def delete_task(id: int) -> bool:
    """
    Deletes a task by its ID.
    Input: id (int) representing the task identifier.
    Output: None on successful deletion.
    Raises ToolError with code 'not_found' if the task does not exist.
    """
    try:
        deleted = task_service.delete_one(query=IdTask(id=id))
        if not deleted:
            raise ToolError(f"Task with ID {id} not found")
        return deleted
    except ToolError:
        raise
    except Exception as e:
        raise ToolError("Unexpected error while deleting task")


if __name__ == "__main__":
    mcp.run(transport="stdio")

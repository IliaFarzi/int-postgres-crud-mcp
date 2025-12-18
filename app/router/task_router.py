from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies import get_task_service
from domain.dto.create_task import CreateTask
from domain.dto.id_task import IdTask
from domain.dto.query_task import QueryTask
from domain.dto.update_task import UpdateTask
from domain.model.task import Task
from service.task_service import TaskService

task_router = APIRouter(prefix="/tasks")


@task_router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: CreateTask, task_service: TaskService = Depends(get_task_service)):
    try:
        return task_service.create_one(payload=payload)
    except Exception as e:
        # Unexpected error
        raise HTTPException(status_code=500, detail=str(e))


@task_router.get("", response_model=List[Task])
def list_tasks(query: QueryTask = Depends(), task_service: TaskService = Depends(get_task_service)):
    try:
        return task_service.read_many(query=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@task_router.get("/{id}", response_model=Task)
def get_task(id: int, task_service: TaskService = Depends(get_task_service)):
    try:
        task = task_service.read_one(query=IdTask(id=id))
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@task_router.patch("/{id}", response_model=Task)
def update_task(id: int, payload: UpdateTask, task_service: TaskService = Depends(get_task_service)):
    try:
        updated = task_service.update_one(query=IdTask(id=id), payload=payload)
        if updated is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated
    except ValueError as ve:
        # E.g., when no fields provided and task not found in fallback select
        raise HTTPException(status_code=404, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@task_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, )
def delete_task(id: int, task_service: TaskService = Depends(get_task_service)):
    try:
        deleted = task_service.delete_one(query=IdTask(id=id))
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        # No content on success
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

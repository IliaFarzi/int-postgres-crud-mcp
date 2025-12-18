from pathlib import Path
from typing import List, Optional, Union

import psycopg
from psycopg.rows import dict_row

from domain.dto.create_task import CreateTask
from domain.dto.id_task import IdTask
from domain.dto.query_task import QueryTask
from domain.dto.update_task import UpdateTask
from domain.model.task import Task


class TaskService:
    def __init__(self, url):
        self.conn = psycopg.connect(url)
        self.table_name = 'tasks'
        self._bootstrap_schema()

    def __del__(self):
        self.close()

    def close(self):
        """Close the underlying DB connection if it's open."""
        if hasattr(self, "conn") and self.conn is not None and not self.conn.closed:
            self.conn.close()

    def _bootstrap_schema(self):
        schema_path = Path(__file__).resolve().parent.parent / "domain" / "db" / "task_schema.sql"
        if not schema_path.exists():
            return
        sql = schema_path.read_text(encoding="utf-8")

        prev_autocommit = getattr(self.conn, "autocommit", False)
        try:
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute(sql)
        finally:
            self.conn.autocommit = prev_autocommit

    @staticmethod
    def row_to_task(row: dict) -> Task:
        return Task.model_validate(row)

    def create_one(self, payload: CreateTask) -> Task:
        # Validate via Pydantic (raises if invalid)
        data = payload.model_dump()
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f"""
                INSERT INTO {self.table_name} (title, description, status)
                VALUES (%s, %s, %s)
                RETURNING id, title, description, status, created_at, updated_at
                """, (data.get('title'), data.get('description'), data.get('status')), )
            row = cur.fetchone()
        self.conn.commit()
        return TaskService.row_to_task(row)

    def read_many(self, query: QueryTask) -> List[Task]:
        clauses = []
        params: List[object] = []
        if query.title is not None:
            clauses.append("title ILIKE %s")
            params.append(f"%{query.title}%")
        if query.description is not None:
            clauses.append("description ILIKE %s")
            params.append(f"%{query.description}%")
        if query.status is not None:
            clauses.append("status = %s")
            params.append(query.status)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT id, title, description, status, created_at, updated_at FROM {self.table_name} {where_sql} ORDER BY id"
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        return [TaskService.row_to_task(r) for r in rows]

    def read_one(self, query: Union[QueryTask, IdTask]) -> Optional[Task]:
        clauses: list[str] = []
        params: list[object] = []

        if isinstance(query, IdTask) and query.id is not None:
            clauses.append("id = %s")
            params.append(query.id)

        if isinstance(query, QueryTask):
            if query.title is not None:
                clauses.append("title ILIKE %s")
                params.append(f"%{query.title}%")

            if query.description is not None:
                clauses.append("description ILIKE %s")
                params.append(f"%{query.description}%")

            if query.status is not None:
                clauses.append("status = %s")
                params.append(query.status)

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""

        sql = f"""
            SELECT id, title, description, status, created_at, updated_at
            FROM {self.table_name}
            {where_sql}
            ORDER BY id
            LIMIT 1
        """

        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(sql, params)
            row = cur.fetchone()

        return TaskService.row_to_task(row) if row else None

    def update_one(self, query: IdTask, payload: UpdateTask) -> Optional[Task]:
        data = payload.model_dump(exclude_unset=True)
        sets = []
        params: List[object] = []
        if 'title' in data and data['title'] is not None:
            sets.append('title = %s')
            params.append(data['title'])
        if 'description' in data:
            sets.append('description = %s')
            params.append(data['description'])
        if 'status' in data and data['status'] is not None:
            sets.append('status = %s')
            params.append(data['status'])

        if not sets:
            with self.conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    f"SELECT id, title, description, status, created_at, updated_at FROM {self.table_name} WHERE id = %s",
                    (query.id,), )
                row = cur.fetchone()
            if row is None:
                raise ValueError(f"Task with id={query.id} not found")
            return TaskService.row_to_task(row)

        set_sql = ', '.join(sets)
        params.append(query.id)
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f"""
                UPDATE {self.table_name}
                SET {set_sql}
                WHERE id = %s
                RETURNING id, title, description, status, created_at, updated_at
                """, params, )
            row = cur.fetchone()
        self.conn.commit()
        return TaskService.row_to_task(row) if row else None

    def delete_one(self, query: IdTask) -> bool:
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE id = %s RETURNING id", (query.id,))
            row = cur.fetchone()
        self.conn.commit()
        return row is not None

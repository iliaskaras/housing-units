from typing import Optional, Any

from pydantic import BaseModel


class TaskStatus(BaseModel):
    task_id: Optional[str]
    task_status: Optional[str]
    task_result: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "task_id": "e3b3326c-617a-4836-8fe0-3c17390f0bd4",
                "task_status": "PENDING",
                "task_result": None,
            }
        }

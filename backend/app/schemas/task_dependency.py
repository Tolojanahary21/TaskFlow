from datetime import datetime

from pydantic import BaseModel,ConfigDict,Field

class TaskDependencyCreate(BaseModel):
    task_id: int  = Field(gt=0)
    depends_on_task_id: int = Field(gt=0)
    dependency_type: str = Field(default="BLOCKS", min_length=1, max_length=50)


class TaskDependencyResponse(BaseModel):
    id: int
    task_id: int
    depends_on_task_id: int
    dependency_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
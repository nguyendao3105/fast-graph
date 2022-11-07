from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BaseModelClass(BaseModel):
    joined: Optional[datetime] = None
    disabled: Optional[bool] = None
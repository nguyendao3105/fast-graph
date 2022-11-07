from typing import Optional
from datetime import datetime

from .base import BaseModelClass

class User(BaseModelClass):
    username: str
    full_name: Optional[str] = None
    joined: Optional[datetime] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str
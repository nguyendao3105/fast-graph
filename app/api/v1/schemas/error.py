from typing import Optional

class BaseResponse:
    code: str
    message: str
    data: Optional[object] = None


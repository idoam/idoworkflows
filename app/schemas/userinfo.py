from datetime import datetime

from pydantic import BaseModel


class UserInfoCreate(BaseModel):
    first_name: str
    last_name: str
    surname: str | None = None
    birth_date: datetime | None = None

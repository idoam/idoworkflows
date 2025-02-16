from datetime import datetime

from sqlmodel import Field, SQLModel


class UserInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    surname: str | None = None
    birth_date: datetime | None = None

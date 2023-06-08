from typing import Optional

from pydantic import BaseModel


class CompanyDetails(BaseModel):
    title: Optional[str]
    description: Optional[str]
    url: str
    links: Optional[list[str]]
    table_data: Optional[list[dict]]
    screenshot: Optional[str]

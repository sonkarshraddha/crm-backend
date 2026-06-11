from pydantic import BaseModel
from typing import Optional


class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str
    priority: Optional[str] = "Medium"


class TicketUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
    priority: Optional[str] = None
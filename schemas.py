from pydantic import BaseModel
from typing import Optional


class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str


class TicketUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
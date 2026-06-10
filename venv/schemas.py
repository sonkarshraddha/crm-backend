from pydantic import BaseModel, EmailStr
from typing import Optional


class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str


class TicketUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
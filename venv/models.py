from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True)

    customer_name = Column(String)
    customer_email = Column(String)

    subject = Column(String)
    description = Column(Text)

    status = Column(String, default="Open")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    note_text = Column(Text)

    created_at = Column(
        DateTime,
        default=func.now()
    )
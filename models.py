from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)

    customer_name = Column(String)
    customer_email = Column(String)
    subject = Column(String)
    description = Column(Text)

    status = Column(String, default="Open")

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    notes = relationship(
        "Note",
        back_populates="ticket"
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id")
    )

    note_text = Column(Text)

    ticket = relationship(
        "Ticket",
        back_populates="notes"
    )
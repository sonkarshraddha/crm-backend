from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Ticket, Note
from schemas import TicketCreate, TicketUpdate
from datetime import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/tickets")
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):
    total_tickets = db.query(Ticket).count()

    new_ticket_id = f"TKT-{total_tickets + 1:03d}"

    new_ticket = Ticket(
        ticket_id=new_ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status="Open",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "ticket_id": new_ticket.ticket_id,
        "created_at": new_ticket.created_at
    }


@router.get("/api/tickets")
def get_tickets(
    status: str = None,
    search: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)

    if status:
        query = query.filter(
            Ticket.status == status
        )

    if search:
        query = query.filter(
            Ticket.customer_name.contains(search)
        )

    tickets = query.all()

    return tickets


@router.get("/api/tickets/{ticket_id}")
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    return ticket


@router.put("/api/tickets/{ticket_id}")
def update_ticket(
    ticket_id: str,
    data: TicketUpdate,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    ticket.status = data.status
    ticket.updated_at = datetime.now()

    if data.notes:
        note = Note(
            ticket_id=ticket.id,
            note_text=data.notes
        )
        db.add(note)

    db.commit()

    return {
        "success": True,
        "updated_at": ticket.updated_at
    }
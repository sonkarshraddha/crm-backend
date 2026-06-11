from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
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


# CREATE TICKET
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
        priority=ticket.priority,
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


# GET ALL TICKETS
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
            or_(
                Ticket.customer_name.contains(search),
                Ticket.subject.contains(search),
                Ticket.ticket_id.contains(search)
            )
        )

    tickets = query.all()

    result = []

    for ticket in tickets:

        ticket_notes = db.query(Note).filter(
            Note.ticket_id == ticket.id
        ).all()

        notes_list = []

        for note in ticket_notes:
            notes_list.append(note.note_text)

        result.append({
            "id": ticket.id,
            "ticket_id": ticket.ticket_id,
            "customer_name": ticket.customer_name,
            "customer_email": ticket.customer_email,
            "subject": ticket.subject,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at,
            "notes": notes_list
        })

    return result


# GET SINGLE TICKET
@router.get("/api/tickets/{ticket_id}")
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    notes = db.query(Note).filter(
        Note.ticket_id == ticket.id
    ).all()

    return {
        "id": ticket.id,
        "ticket_id": ticket.ticket_id,
        "customer_name": ticket.customer_name,
        "customer_email": ticket.customer_email,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "notes": [n.note_text for n in notes]
    }


# UPDATE TICKET
@router.put("/api/tickets/{ticket_id}")
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    ticket.status = data.status

    if data.priority:
        ticket.priority = data.priority

    ticket.updated_at = datetime.now()

    if data.notes and data.notes.strip() != "":
        note = Note(
            ticket_id=ticket.id,
            note_text=data.notes
        )

        db.add(note)

    db.commit()

    return {
        "success": True
    }


# DELETE TICKET
@router.delete("/api/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):

    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully"
    }


# DASHBOARD STATS
@router.get("/api/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    total = db.query(Ticket).count()

    open_count = db.query(Ticket).filter(
        Ticket.status == "Open"
    ).count()

    closed_count = db.query(Ticket).filter(
        Ticket.status == "Closed"
    ).count()

    progress_count = db.query(Ticket).filter(
        Ticket.status == "In Progress"
    ).count()

    return {
        "total": total,
        "open": open_count,
        "closed": closed_count,
        "in_progress": progress_count
    }
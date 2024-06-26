from datetime import datetime, timedelta

from typing import List

from sqlalchemy import or_, and_, extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdateSchema


# async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
#     return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contacts_by_params(name: str, surname: str, email: str, skip: int, limit: int, db: Session) -> List[Contact]:
    if name or surname or email:
        return db.query(Contact).filter(or_(Contact.name == name, Contact.surname == surname, Contact.email == email)).offset(skip).limit(limit).all()
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_birthdays_in_7_days(db: Session) -> List[Contact]:
    today = datetime.now().date()
    end_date = today + timedelta(days=7)

    contact = (
        db.query(Contact)
        .filter(and_(
                    extract("month", Contact.birthday) == today.month,
                    extract("day", Contact.birthday) >= today.day,
                    extract("day", Contact.birthday) <= end_date.day,
                ),
            )
        
        .all()
    )
    return contact


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, 
                   phonenumber=body.phonenumber, birthday=body.birthday, description=body.description)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdateSchema, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phonenumber = body.phonenumber
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact

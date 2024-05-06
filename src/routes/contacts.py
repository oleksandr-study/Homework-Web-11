from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdateSchema, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["Contacts"])


# @router.get("/all/", response_model=List[ContactResponse])
# async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     contact = await repository_contacts.get_contacts(skip, limit, db)
#     return contact


@router.get("/", response_model=List[ContactResponse])
async def read_contacts_by_params(name: str = None, surname: str = None, email: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contacts_by_params(name, surname, email, skip, limit, db)
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdateSchema, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/birthdays/", response_model=List[ContactResponse])
async def birthdays_in_7_days(db: Session = Depends(get_db)):
    contact = await repository_contacts.get_birthdays_in_7_days(db)
    return contact
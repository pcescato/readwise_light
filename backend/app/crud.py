from sqlmodel import Session, select
from . import models

def create_document(session: Session, doc: models.Document):
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc

def get_document(session: Session, doc_id: int):
    return session.get(models.Document, doc_id)

def get_all_documents(session: Session):
    return session.exec(select(models.Document)).all()

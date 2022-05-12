from sqlalchemy.orm import Session
import models, schemas


def get_member_by_id(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_member_by_name(db: Session, member_name: str):
    return db.query(models.Member).filter(models.Member.name == member_name).first()


def get_all_members(db: Session):
    return db.query(models.Member).all()


def create_member(db: Session, member: schemas.CreateMember):
    db_member = models.Member(name=member.name)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    db_member.msg = "New City Council member added."
    return db_member

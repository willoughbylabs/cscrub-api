from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/members/", response_model=schemas.Member)
def read_all_members(db: Session = Depends(get_db)):
    members = crud.get_all_members(db)
    return members


@app.post("/members/", response_model=schemas.Member)
def create_member(member: schemas.CreateMember, db: Session = Depends(get_db)):
    db_user = crud.get_member_by_name(db, member_name=member.name)
    if db_user:
        return {
            "id": db_user.id,
            "name": db_user.name,
            "msg": "City Council member already in database. Skipping...",
        }
    return crud.create_member(db=db, member=member)

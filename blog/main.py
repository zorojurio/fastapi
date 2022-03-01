from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
print("creating")
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blogs/')
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    print(new_blog)
    return new_blog



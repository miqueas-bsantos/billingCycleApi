from model import Schemas
from typing import Dict
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy.orm import Session
import model

class TodoModel(Base):
    __tablename__="TODO"
    id = Column(Integer, primary_key= True, autoincrement=True)
    description = Column(String(80))
    isDone = Column('is_done', Boolean)

    @classmethod
    def find_by_id(cls, db: Session, user_id: int) -> "TodoModel":
        return db.query(cls).filter(cls.id==user_id).first()

    def delete_from_db(self, db: Session):
        db.delete(self)
        db.commit()

    def save_to_db(self, db: Session) -> None:
        # db_item = TodoModel(**todo.dict())
        # db.add(db_item)
        # db.commit()
        # db.refresh(db_item)       
        db.add(self)
        db.commit()
    
    @classmethod
    def update_db(cls, db: Session, todo: Schemas.Todo) -> bool:
        current = db.query(TodoModel)\
                    .filter(TodoModel.id == todo.id)\
                    .first()
        if current:
            current.description = todo.description
            current.isDone = todo.isDone
            db.commit()
            return True
        return False

    @classmethod
    def find_all(cls, db: Session, description=''):
        resp = db.query(cls)
        if description:
            resp = resp.filter(TodoModel.description.ilike(f'%{description}%'))
        return resp.all()

    def json(self) -> Dict:
        return { 
            "id": self.id, 
            "description": self.description, 
            "isDone": self.is_done 
        }
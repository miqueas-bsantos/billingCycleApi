from sqlalchemy.sql.sqltypes import Numeric
from model import Schemas
from typing import Dict
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, func)
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy.orm import Session, relationship


class BilligCycle(Base):
    __tablename__="TB_BILLIGCYCLE"
    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(80))
    month = Column(Integer)
    year = Column(Integer)
    debits = relationship("Debits", cascade="delete",  lazy="joined")
    credits = relationship("Credits", cascade="delete",  lazy="joined")

    @classmethod
    def find_all(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def find_summary(cls, db: Session):
        response = db.query(func.sum(Debits.value).label("debit"), func.sum(Credits.value).label("credit")).select_from(cls).join(Credits).join(Debits).first()
        return response

    def save_to_db(self, db: Session) -> None:   
        db.add_all(self.debits)
        db.add_all(self.credits)
        db.add(self)
        db.commit()

    def update(self, db: Session) -> None:
        item = db.query(BilligCycle).filter(BilligCycle.id == self.id).first()
        if item:
            item.month = self.month
            item.year = self.year
            item.name = self.name
            db.commit()

    def delete_by_id(self, db: Session, id: int) -> None:
        item = db.query(BilligCycle).filter(BilligCycle.id == id).first()
        if item:
            db.delete(item)
            db.commit()


class Credits(Base):
    __tablename__="TB_CREDITS"
    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(80))
    status = Column(String(30))
    value = Column(Numeric)
    billingCycleId  = Column(Integer, ForeignKey('TB_BILLIGCYCLE.id'), nullable=False)

class Debits(Base):
    __tablename__="TB_DEBITS"
    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(80))
    status = Column(String(30))
    value = Column(Numeric)
    billingCycleId  = Column(Integer, ForeignKey('TB_BILLIGCYCLE.id'), nullable=False)



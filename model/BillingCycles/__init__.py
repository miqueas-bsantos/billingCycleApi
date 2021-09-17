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
        for debit in self.debits:
            debit.id = None
        for debit in self.credits:
            debit.id = None
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
            list_to_keep = []
            
            for credit in self.credits:
                is_there = next(filter(lambda x: x.id == credit.id, item.credits), None)
                if is_there and credit.id != -1:
                    is_there.name = credit.name
                    is_there.value = credit.value
                    list_to_keep.append(is_there.id)
                elif credit.id == -1:
                    credit.id = None
                    db.add(credit)
                    db.commit()
                    item.credits.append(credit)
                    list_to_keep.append(credit.id)

            db.query(Credits).filter(Credits.id.notin_(list_to_keep), 
                        Credits.billingCycleId==item.id).delete(synchronize_session=False)

            list_to_keep = []
            for debit in self.debits:
                is_there = next(filter(lambda x: x.id == debit.id, item.debits), None)
                if is_there and debit.id != -1:
                    is_there.name = debit.name
                    is_there.value = debit.value
                    is_there.status = debit.status
                    list_to_keep.append(is_there.id)
                elif debit.id == -1:
                    debit.id = None
                    db.add(debit)
                    db.commit()
                    item.debits.append(debit)
                    list_to_keep.append(debit.id)

            db.query(Debits).filter(Debits.id.notin_(list_to_keep), 
                        Debits.billingCycleId==item.id).delete(synchronize_session=False)

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



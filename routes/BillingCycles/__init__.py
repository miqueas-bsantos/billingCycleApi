from fastapi.security import HTTPBasic
from fastapi import APIRouter, Depends, HTTPException, status
from model import (
     TodoModel, 
     ModelSchemas,
     CreditModel,
     DebitModel,
     BillingCyclesModel
)
from services import Cognito
from typing import Any, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

router  = APIRouter()
security = HTTPBasic()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost/dev/api/user/authentication")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = Cognito().get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Optional[Any] = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
        
@router.post("/billingCycles", description="Save credits or debits")
async def create_billing_cycle(billingCycle: ModelSchemas.BillingCycleCreate, db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        payload = billingCycle.dict()
        debits = [DebitModel(**debits) for debits in payload['debits']]
        credits = [CreditModel(**credits) for credits in payload['credits']]
        del payload["credits"]
        del payload["debits"]
        billingCycle = BillingCyclesModel(**payload)
        billingCycle.debits = debits
        billingCycle.credits = credits

        billingCycle.save_to_db(db)
        response["data"] = billingCycle.find_all(db)
        return response
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response
        )

@router.put("/billingCycles", description="Update billingCycles")
async def update_billing_cycle(billingCycle: ModelSchemas.BillingCycleCreate, db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        payload = billingCycle.dict()
        debits = [DebitModel(**debits) for debits in payload['debits']]
        credits = [CreditModel(**credits) for credits in payload['credits']]
        del payload["credits"]
        del payload["debits"]
        billingCycle = BillingCyclesModel(**payload)
        billingCycle.debits = debits
        billingCycle.credits = credits

        billingCycle.update(db)
        response["data"] = billingCycle.find_all(db)
        return response
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response
        )

@router.delete("/billingCycles/{id}", description="Delete the given Id billingCycles")
async def delete_billing_cycle(id: int, db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        billingCycle = BillingCyclesModel()
        billingCycle.delete_by_id(db, id)
        response["data"] = billingCycle.find_all(db)
        return response
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=response
        )

@router.get("/billingCycles", description="Save credits or debits")
async def get_billing_cycle(db: Session = Depends(get_db), token: str = Depends(get_current_active_user)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        billingCycle = BillingCyclesModel()
        response["data"] = billingCycle.find_all(db)
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=response["statusCode"],
            detail=response
        )
    finally:
        return response

@router.get("/billingCycles/summary", description="Save credits or debits")
async def get_billing_cycle(db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": {},
        "errors": None
    }
    try:
        debit, credit = BillingCyclesModel().find_summary(db)
        response["data"] = {"debit": debit, "credit": credit}
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=response["statusCode"],
            detail=response
        )
    finally:
        return response
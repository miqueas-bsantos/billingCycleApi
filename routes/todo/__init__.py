from fastapi.security import HTTPBasic
from fastapi import APIRouter, Depends, HTTPException, status
from model import TodoModel, ModelSchemas
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal

router  = APIRouter()
security = HTTPBasic()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todo", description="function test")
async def create_todo(todo: ModelSchemas.TodoCreate, db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        my_todo = TodoModel(**todo.dict())
        my_todo.save_to_db(db)
        response["data"] = TodoModel.find_all(db)
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=response["statusCode"],
            detail=response
        )
    finally:
        return response

@router.put("/todo")
async def update_todo(todo: ModelSchemas.Todo, db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        response["errros"] = None if TodoModel.update_db(db=db, todo=todo) else "Not found"
        response["data"] = TodoModel.find_all(db)
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=response["statusCode"],
            detail=response
        )
    finally:
        return response

@router.delete("/todo/{id}")
async def delete_todo(id: int, db: Session = Depends(get_db)):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        todo = TodoModel.find_by_id(db, id)
        if todo:
            todo.delete_from_db(db)
        response["data"] = TodoModel.find_all(db)
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=response["statusCode"],
            detail=response
        )
    finally:
        return response

@router.get("/todo")
async def describe_todo(db: Session = Depends(get_db), description: Optional[str] = None):
    response = {
        "statusCode": 200,
        "data": [],
        "errors": None
    }
    try:
        response["data"] = TodoModel.find_all(db, description=description)
    except Exception as error:
        response["errors"] = str(error)
        response["statusCode"]=status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=response["statusCode"],
            detail=response
        )
    finally:
        return response
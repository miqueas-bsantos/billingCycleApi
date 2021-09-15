from fastapi import FastAPI
from routes import TodoRoutes, BillingCyclesRoutes
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url="/billingCycles/docs", redoc_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
# app.include_router(TodoRoutes.router)
app.include_router(BillingCyclesRoutes.router)

# Adyen
# Ame deploy CI/CD
# Suporte API externa
# Atividade da V4
# Stone
from fastapi import FastAPI
from database import Base, engine
import auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include auth routes
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "api.willgob.com backend is running"}

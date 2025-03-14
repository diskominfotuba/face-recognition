from fastapi import FastAPI
import uvicorn
from .routes import router
from .db import SessionLocal, Face

app = FastAPI()

# Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

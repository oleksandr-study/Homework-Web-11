from fastapi import FastAPI

from src.routes import contacts

app = FastAPI()

app.include_router(contacts.router)


@app.get("/")
def main_root():
    return {"message": "Contacts application"}
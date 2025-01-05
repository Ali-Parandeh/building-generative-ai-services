from fastapi import FastAPI, Depends


def get_db():
    db = ...  # create a database session
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/users/{email}/messages")
def get_user_messages(email, db=Depends(get_db)):
    user = db.query(...)  # db is reused
    messages = db.query(...)  # db is reused
    return messages

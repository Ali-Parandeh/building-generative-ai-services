from fastapi import FastAPI, Depends


def get_db():
    db = ...  # create a database session
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
def get_user_messages(db=Depends(get_db)):
    user = db.query(...)  # db is reused
    messages = db.query(...)  # db is reused
    return messages

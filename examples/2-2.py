from fastapi import FastAPI, Depends


def check_age(age: int) -> bool:
    return age >= 18


app = FastAPI()

app.get("/")


def check_age_controller(is_adult: bool = Depends(check_age)):
    return is_adult

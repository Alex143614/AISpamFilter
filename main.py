from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "Filter"))

from filters import (
    get_all_emails,
    find_by_sender,
    create_email,
    rate_email,
    avg_user_score,
    get_emails_from_db,
    load_emails_to_db,
)

app = FastAPI()


class EmailIn(BaseModel):
    sender: str
    text: str


class RateIn(BaseModel):
    email_id: int
    my_score: int


@app.get("/emails")
def emails():
    result = []
    for e in get_emails_from_db():
        result.append({
            "id": e.id,
            "sender": e.sender,
            "text": e.text,
            "time": e.time,
            "classification": e.classification,
            "confidence": e.confidence,
            "reasons": e.reasons,
            "created_at": e.created_at,
        })
    return result


@app.get("/search")
def search(sender: str):
    return find_by_sender(sender, get_all_emails(), None)


@app.post("/emails")
def add_email(data: EmailIn):
    email = create_email(data.sender, data.text)
    return {
        "id": email.id,
        "sender": email.sender,
        "text": email.text,
        "classification": email.classification,
        "confidence": email.confidence,
        "reasons": email.reasons,
        "created_at": email.created_at,
    }


@app.post("/rate")
def rate(data: RateIn):
    stat = rate_email(data.email_id, data.my_score)
    if stat is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return {
        "id": stat.id,
        "sender": stat.sender,
        "text": stat.text,
        "scores": stat.scores,
        "created_at": stat.created_at,
    }


@app.get("/avg")
def avg():
    return {"avg_score": avg_user_score()}


@app.post("/load")
def load():
    return {"loaded": load_emails_to_db()}
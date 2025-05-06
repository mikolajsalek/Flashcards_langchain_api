from fastapi import APIRouter, Form
from app.schemas import TextRequest
from app.summarizer import summarize_text
from app.summarizer import generate_flashcards


router = APIRouter()

@router.post("/summarize")
async def summarize(content: str = Form(...), mode: str = Form(...)):
    result = summarize_text(content, mode)
    return {"result": result}

@router.post("/generate_flashcards")
async def generate_flashcards_route(content: str):
    flashcards = generate_flashcards(content)
    return {"flashcards": flashcards}
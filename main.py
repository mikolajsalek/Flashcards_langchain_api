from fastapi import FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.summarizer import summarize_text
from app.flashcards_generator import generate_flashcards

import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

flashcards_content = {}

class SummaryRequest(BaseModel):
    content: str
    mode: str = "summary"


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})



@app.post("/summarize", response_class=HTMLResponse)
async def summarize(request: Request, content: str = Form(...), mode: str = Form(...)):
    global flashcards_content
    try:
        result = summarize_text(content, mode)
        if mode == 'flashcards':
            flashcards_content = result
            #print(flashcards_content)
    except Exception as e:
        result = f"Wystąpił błąd: {str(e)}"
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "content": content,
            "mode": mode,
            "result": result
        }
    )

@app.get("/flashcards", response_class=HTMLResponse)
async def flashcards(request: Request, content: str = Query(default="Placeholder")):
    global flashcards_content

    print("Flashcards:", flashcards_content)  # Upewnij się, że są dane

    return templates.TemplateResponse("flashcards.html", {
        "request": request,
        "flashcards": flashcards_content
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

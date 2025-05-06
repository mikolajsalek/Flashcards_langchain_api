from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

load_dotenv()

llm = ChatGroq(
    temperature=0.3,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

PROMPTS = {
    "summary": "Stwórz krótkie streszczenie poniższego tekstu:\n{content}",
    "bullet-points": "Zamień poniższy tekst na listę wypunktowaną z kluczowymi informacjami:\n{content}",
    "flashcards": "Proszę wygenerować fiszki w formacie "'Pytanie: ... Odpowiedź: ...'" na podstawie poniższego tekstu: {content}, w odpowiedzi uwzględnij tylko pytania i odpowiedzi"
}


def summarize_text(content: str, mode: str):
    prompt = PROMPTS.get(mode, PROMPTS["summary"]).format(content=content)
    response = llm.predict(prompt)
    
    if mode == "bullet-points":
        response = response.replace("*", "•")
    elif mode == 'flashcards':
        return parse_flashcards(response)

    return response

def parse_flashcards(text: str) -> dict:
    flashcards = {}
    pairs = re.findall(r"Pytanie:\s*(.*?)\nOdpowiedź:\s*(.*?)(?:\n|$)", text, re.DOTALL)
    for question, answer in pairs:
        flashcards[question.strip()] = answer.strip()
    return flashcards
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    temperature=0.3,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

PROMPTS = {
    "summary": "Stwórz krótkie streszczenie poniższego tekstu:\n{content}",
    "bullet-points": "Zamień poniższy tekst na listę wypunktowaną z kluczowymi informacjami:\n{content}",
    "flashcards": "Na podstawie poniższego tekstu wygeneruj fiszki w formacie:\nPytanie: ...\nOdpowiedź: ...\n\nTekst:\n{content}"
}


def summarize_text(content: str, mode: str):
    prompt = PROMPTS.get(mode, PROMPTS["summary"]).format(content=content)
    response = llm.predict(prompt)
    
    if mode == "bullet-points":
        response = response.replace("*", "•")


    return response

def generate_flashcards(content: str):
    points = content.split("\n")  # Rozdzielamy punktu na oddzielne linie
    flashcards = []

    for point in points:
        question = f"Co oznacza: {point}?"
        answer = f"To: {point}"
        flashcards.append({"question": question, "answer": answer})

    return flashcards

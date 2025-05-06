def generate_flashcards(content: str):
    points = content.split("\n")  
    flashcards = []

    for point in points:
        question = f"Co oznacza: {point}?"
        answer = f"To: {point}"
        flashcards.append({"question": question, "answer": answer})

    return flashcards
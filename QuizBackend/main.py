from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API Quiz pour Android")

# 1. Modèle de données pour une Question 
class Question(BaseModel):
    id: int
    question_text: str
    option1: str
    option2: str
    option3: str
    correct_answer: int  # Numéro de la bonne option (1, 2 ou 3)

# 2. Base de données fictive en mémoire locale (Mise à jour avec 4 questions stables)
fake_questions_db = [
    {
        "id": 1,
        "question_text": "Quelle est la capitale du Maroc ?",
        "option1": "Casablanca",
        "option2": "Rabat",
        "option3": "Marrakech",
        "correct_answer": 2
    },
    {
        "id": 2,
        "question_text": "Quel langage utilise-t-on nativement pour Android ?",
        "option1": "Python",
        "option2": "Java/Kotlin",
        "option3": "PHP",
        "correct_answer": 2
    },
    {
        "id": 3,
        "question_text": "Planète la plus proche du Soleil ?",
        "option1": "La Terre",
        "option2": "Mercure",
        "option3": "Mars",
        "correct_answer": 2
    },
    {
        "id": 4,
        "question_text": "Combien de cœurs possède une pieuvre ?",
        "option1": "1 cœur",
        "option2": "2 cœurs",
        "option3": "3 cœurs",
        "correct_answer": 3
    }
]

# ====================================================
# GESTION DES ROUTES (GET, POST, PUT, DELETE) http://172.20.10.9:8000/questions
# ====================================================

# 📌 ROUTE 1 : GET - Récupérer toutes les questions
@app.get("/questions", response_model=List[Question])
def get_all_questions():
    return fake_questions_db

# 📌 ROUTE 2 : POST - Ajouter une nouvelle question (via Swagger UI /docs)
@app.post("/questions", response_model=Question, status_code=201)
def create_question(question: Question):
    for q in fake_questions_db:
        if q["id"] == question.id:
            raise HTTPException(status_code=400, detail="Une question avec cet ID existe déjà.")
    
    new_q = question.dict()
    fake_questions_db.append(new_q)
    return new_q

# 📌 ROUTE 3 : PUT - Modifier une question existante
@app.put("/questions/{question_id}", response_model=Question)
def update_question(question_id: int, updated_question: Question):
    for index, q in enumerate(fake_questions_db):
        if q["id"] == question_id:
            fake_questions_db[index] = updated_question.dict()
            return fake_questions_db[index]
            
    raise HTTPException(status_code=404, detail="Question non trouvée.")

# 📌 ROUTE 4 : DELETE - Supprimer une question
@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    for index, q in enumerate(fake_questions_db):
        if q["id"] == question_id:
            fake_questions_db.pop(index)
            return {"message": f"La question {question_id} a été supprimée avec succès !"}
            
    raise HTTPException(status_code=404, detail="Question non trouvée.")
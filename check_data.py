from app import app, db
from models import Category, Question

with app.app_context():
    categories = Category.query.all()
    for cat in categories:
        print("Category:", cat.name)

    questions = Question.query.all()
    for q in questions:
        print("Question:", q.question_text, "| Category:", q.category)

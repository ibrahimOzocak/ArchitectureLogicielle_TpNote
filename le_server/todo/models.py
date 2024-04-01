from .app import db
from flask import url_for

class Questionnaire(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"<Questionnaire {self.id}, {self.name}>"
    
    def create(name):
        questionnaire = Questionnaire(name)
        db.session.add(questionnaire)
        db.session.commit()
        return questionnaire.to_json()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "url_questions": url_for('get_questionnaire', id=self.id, _external=True)
        }
    
    def get_questions_by_questionnaire(id_questionnaire):
        return Question.query.filter_by(questionnaire_id=id_questionnaire).all()

    def get_questionnaire(id):
        questionnaire = Questionnaire.query.get(id)
        if questionnaire is None:
            return None
        return questionnaire.to_json()

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=False)
    questionnaire = db.relationship('Questionnaire', backref=db.backref('questions', lazy=True))

    def __repr__(self) -> str:
        return f"<Question {self.id}, {self.title}, {self.questionnaire_id}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "questionnaire_id": self.questionnaire_id,
            "url_question": url_for('get_question', id=self.questionnaire_id, question_id=self.id, _external=True) + ' ou ' + url_for('get_question_2', id=self.id, _external=True)
        }

    @classmethod
    def create(cls, title, questionnaire_id):
        question = cls(title=title, questionnaire_id=questionnaire_id)
        db.session.add(question)
        db.session.commit()
        return question.to_json()
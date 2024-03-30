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
        return {
            "id": questionnaire.id,
            "name": questionnaire.name,
            'questions':[question.to_json() for question in questionnaire.questions]
        }

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionType = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=False)
    questionnaire = db.relationship('Questionnaire', backref=db.backref('questions', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity':'question',
        "with_polymorphic": "*",
        'polymorphic_on': questionType
    }
    
    def __repr__(self) -> str:
        return f"<Question {self.id}, {self.title}, {self.questionType}, {self.questionnaire_id}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "questionType": self.questionType,
            "questionnaire_id": self.questionnaire_id
        }

class QuestionS(Question):
    __tablename__ = 'questionS'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    question = db.Column(db.String(120))
    answer = db.Column(db.String(120))

    __mapper_args__ = {
        'polymorphic_identity':'questionS',
        "with_polymorphic": "*",
        'polymorphic_load': 'inline'
    }

    def __init__(self, title, question, answer, questionnaire_id):
        super().__init__(title=title, questionType="questionS", questionnaire_id=questionnaire_id)
        self.title = title
        self.question = question
        self.answer = answer
        self.questionnaire_id = questionnaire_id

    def __repr__(self) -> str:
        return f"<QuestionS {self.id}, {self.title}, {self.question}, {self.answer}, {self.questionnaire_id}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "question": self.question,
            "answer": self.answer,
            "question_type": "questionS",
            "questionnaire_id": self.questionnaire_id,
            "url_question": url_for('get_question', id=self.questionnaire_id, question_id=self.id, _external=True) + ' ou ' + url_for('get_question_2', id=self.id, _external=True)
        }

    def create(title, question, answer, questionnaire_id):
        questionS = QuestionS(title, question, answer, questionnaire_id)
        db.session.add(questionS)
        db.session.commit()
        return questionS.to_json()

class QuestionM(Question):
    __tablename__ = 'questionM'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    question = db.Column(db.String(120))
    answers = db.Column(db.String(120))

    __mapper_args__ = {
        'polymorphic_identity':'questionM',
        "with_polymorphic": "*",
        'polymorphic_load': 'inline'
    }

    def __init__(self, title, question, answers, questionnaire_id):
        super().__init__(title=title, questionType="questionM", questionnaire_id=questionnaire_id)
        self.title = title
        self.question = question
        self.answers = answers
        self.questionnaire_id = questionnaire_id

    def __repr__(self) -> str:
        return f"<questionM {self.id}, {self.title}, {self.question}, {self.answers}, {self.questionnaire_id}>"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "question": self.question,
            "answers": self.answers,
            "question_type": "questionM",
            "questionnaire_id": self.questionnaire_id,
            "url_question": url_for('get_question', id=self.questionnaire_id, question_id=self.id, _external=True) + ' ou ' + url_for('get_question_2', id=self.id, _external=True)
        }

    def create(title, question, answers, questionnaire_id):
        questionM = questionM(title, question, answers, questionnaire_id)
        db.session.add(questionM)
        db.session.commit()
        return questionM.to_json()

tasks = [
    {
        'id': 1,
        'title': 'Courses',
        'description': 'Salade, Oignons, Pommes, Clementines',
        'done': True
    },
    {
        'id': 2,
        'title': 'Apprendre REST',
        'description': 'Apprendre mon cours et comprendre les exemples',
        'done': False
    },
    {
        'id': 3,
        'title': 'Apprendre Ajax',
        'description': 'Revoir les exemples et écrire un client REST JS avec Ajax',
        'done': False
    }
]
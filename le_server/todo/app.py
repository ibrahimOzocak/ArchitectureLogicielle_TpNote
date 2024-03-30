from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, ressources={r"/todo/api/v1.0/*":{"origins":"*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

from .models import Questionnaire, Question
with app.app_context():
    print("Dropping database...")
    db.drop_all()
    print("Creating database...")
    db.create_all()
    print("Creating questionnaires...")
    db.session.add_all(
        [
            Questionnaire(name='Courses'),
            Questionnaire(name='Apprendre REST'),
            Questionnaire(name='Apprendre Ajax')
        ]
    )
    db.session.commit()
    print("Creating questions...")
    db.session.add_all(
        [
            Question(title='Fraises', questionnaire_id=1),
            Question(title='Oignons', questionnaire_id=1),
            Question(title='Pommes', questionnaire_id=1),
            Question(title='Clementines', questionnaire_id=1),
            Question(title='Apprendre mon cours et comprendre les exemples', questionnaire_id=2),
            Question(title='Revoir les exemples et écrire un client REST JS avec Ajax', questionnaire_id=3)
        ]
    )
    db.session.commit()

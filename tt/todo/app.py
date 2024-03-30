from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, ressources={r"/todo/api/v1.0/*":{"origins":"*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

from .models import Questionnaire, QuestionS, QuestionM
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
            QuestionS(title='Salade', question='text', answer="test", questionnaire_id=1),
            QuestionS(title='Oignons', question='text', answer="TT", questionnaire_id=1),
            QuestionS(title='Pommes', question='text', answer="BLABLA", questionnaire_id=1),
            QuestionM(title='Clementines', question='text', answers="T T T", questionnaire_id=1),
            QuestionM(title='Apprendre mon cours et comprendre les exemples', question='text', answers="E E",questionnaire_id=2),
            QuestionM(title='Revoir les exemples et écrire un client REST JS avec Ajax', question='text', answers="S",questionnaire_id=3)
        ]
    )
    db.session.commit()

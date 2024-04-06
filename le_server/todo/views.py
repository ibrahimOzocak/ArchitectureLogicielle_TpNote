from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import Question, Questionnaire, db


# GET /questionnaires
@app.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = [questionnaire.to_json() for questionnaire in Questionnaire.query.all()]
    for questionnaire in questionnaires:
        questionnaire['url_questions'] = url_for('get_questionnaire', id=questionnaire['id'], _external=True)
    return jsonify({'questionnaires': questionnaires})

# GET /questionnaires/<int:id>
@app.route('/questionnaires/<int:id>', methods=['GET'])
def get_questionnaire(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    return jsonify(questionnaire)

# GET /questionnaires/<int:id>/questions/<int:id>
@app.route('/questionnaires/<int:id>/questions/<int:question_id>', methods=['GET'])
def get_question(id, question_id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    return jsonify(question.to_json())

# GET /questionnaires/<int:id>/questions
@app.route('/questionnaires/<int:id>/questions', methods=['GET'])
def get_questions(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    return jsonify({'questions': [question.to_json() for question in Questionnaire.get_questions_by_questionnaire(questionnaire['id'])]})

# GET /questions/<int:id>
@app.route('/questions/<int:id>', methods=['GET'])
def get_question_avec_id(id):
    question = Question.query.get(id)
    if question is None:
        abort(404)
    return jsonify(question.to_json())

# POST /questionnaires
@app.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    if not request.json or not 'name' in request.json:
        # si la requête n'est pas au format JSON ou si elle ne contient pas de champ 'name'
        abort(400)
    return jsonify(Questionnaire.create(request.json['name'])), 201

# POST /questionnaires/<int:id>/questions
@app.route('/questionnaires/<int:id>/questions', methods=['POST'])
def create_question(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    if not request.json or not 'title' in request.json:
        abort(400)
    title = request.json['title']
    questionnaire_id = questionnaire['id']
    question = Question(title=title, questionnaire_id=questionnaire_id)
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_json()), 201

# PUT /questionnaires/<int:id>
@app.route('/questionnaires/<int:id>', methods=['PUT'])
def modif_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    new_name = request.json.get('name')
    if new_name and isinstance(new_name, str):
        questionnaire.name = new_name
        db.session.commit()
        return jsonify(questionnaire.to_json()), 201
    else:
        abort(400)

# PUT /questionnaires/<int:id>/questions/<int:id>
@app.route('/questionnaires/<int:id>/questions/<int:question_id>', methods=['PUT'])
def modif_question(id, question_id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'questionType' in request.json and type(request.json['questionType']) != str:
        abort(400)
    question.title = request.json.get('title', question.title)
    db.session.commit()
    return jsonify(question.to_json())


# DELETE /questionnaires/<int:id>
@app.route('/questionnaires/<int:id>', methods=['DELETE'])
def delete_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    print(questionnaire)
    if questionnaire is None:
        abort(404)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({'result': True})

# DELETE /questionnaires/<int:id>/questions/<int:id>
@app.route('/questionnaires/<int:id>/questions/<int:question_id>', methods=['DELETE'])
def delete_question(id, question_id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'result': True})
from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import tasks, Question, Questionnaire, db

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['id'] = task['id']
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json or not 'description' in request.json:
        # si la requête n'est pas au format JSON ou si elle ne contient pas de champ 'title' / 'description'
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1, # on récupère l'id de la dernière tâche et on l'incrémente de 1
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': request.json.get('done', False)
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # on récupère la tâche dont l'id est task_id
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        # si la tâche n'existe pas, on retourne une erreur 404
        abort(404)
    if not request.json:
        # si la requête n'est pas au format JSON, on retourne une erreur 400
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        # si le champ 'title' n'est pas une chaîne de caractères, on retourne une erreur 400
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        # si le champ 'description' n'est pas une chaîne de caractères, on retourne une erreur 400
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        # si le champ 'done' n'est pas un booléen, on retourne une erreur 400
        abort(400)
    # on met à jour la tâche
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    # on retourne la tâche mise à jour
    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # on récupère la tâche dont l'id est task_id
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        # si la tâche n'existe pas, on retourne une erreur 404
        abort(404)
    # on supprime la tâche
    tasks.remove(task[0])
    # on retourne un message de succès
    return jsonify({'result': True})

# faire une api qui permet de gérer des questionnaires

# GET /questionnaires
@app.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = [questionnaire.to_json() for questionnaire in Questionnaire.query.all()]

    for questionnaire in questionnaires:
        questionnaire['url_questions'] = url_for('get_questionnaire', id=questionnaire['id'], _external=True)

    return jsonify({'questionnaires': questionnaires})

# POST /questionnaires
@app.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    if not request.json or not 'name' in request.json:
        # si la requête n'est pas au format JSON ou si elle ne contient pas de champ 'name'
        abort(400)
    return jsonify(Questionnaire.create(request.json['name'])), 201

# GET /questionnaires/<int:id>
@app.route('/questionnaires/<int:id>', methods=['GET'])
def get_questionnaire(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    return jsonify(questionnaire)

# PUT /questionnaires/<int:id>
@app.route('/questionnaires/<int:id>', methods=['PUT'])
def update_questionnaire(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    questionnaire.name = request.json.get('name', questionnaire.name)
    db.session.commit()
    return jsonify(questionnaire.to_json())

# DELETE /questionnaires/<int:id>
@app.route('/questionnaires/<int:id>', methods=['DELETE'])
def delete_questionnaire(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({'result': True})

# GET /questionnaires/<int:id>/questions
@app.route('/questionnaires/<int:id>/questions', methods=['GET'])
def get_questions(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    return jsonify({'questions': [question.to_json() for question in Questionnaire.get_questions_by_questionnaire(questionnaire['id'])]})

# POST /questionnaires/<int:id>/questions
@app.route('/questionnaires/<int:id>/questions', methods=['POST'])
def create_question(id):
    questionnaire = Questionnaire.get_questionnaire(id)
    if questionnaire is None:
        abort(404)
    if not request.json or not 'title' in request.json or not 'questionType' in request.json:
        abort(400)
    question = Question(request.json['title'], request.json['questionType'], questionnaire.id)
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_json()), 201

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

# GET /questions/<int:id>
@app.route('/questions/<int:id>', methods=['GET'])
def get_question_2(id):
    question = Question.query.get(id)
    if question is None:
        abort(404)
    return jsonify(question.to_json())

# PUT /questionnaires/<int:id>/questions/<int:id>
@app.route('/questionnaires/<int:id>/questions/<int:question_id>', methods=['PUT'])
def update_question(id, question_id):
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
    question.questionType = request.json.get('questionType', question.questionType)
    db.session.commit()
    return jsonify(question.to_json())

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
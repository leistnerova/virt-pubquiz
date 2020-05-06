from flask import request, render_template
from flask_restplus import Namespace, Resource

from .. import db
from ..model import Categories, QuestionsAll, QuizRun, Teams
from ..utils.quiz import QuizFactory
from ..utils.team import Answer

play_ns = Namespace('play', description="Endpoint to retrieve play information")


@play_ns.route('/actual')
class PlayActual(Resource):
    def get(self):
        res = {'question_id': '-1'}
        quiz = QuizFactory().get_actual_quiz()
        run = db.session.query(QuizRun).first()
        if run:
            if run.show_category_id:
                item = db.session.query(Categories).filter_by(category_id=run.show_category_id).first()
                item.title = item.name
                res['question_id'] = '-2'
                res['html'] = render_template('run/item.html', item=item)
            else:
                if quiz.is_active:
                    item = db.session.query(QuestionsAll).filter_by(question_id=run.question_actual).first()
                    res['question_id'] = item.question_id
                    item.actual = True
                    res['html'] = render_template('run/item.html', item=item)
                else:
                    res['html'] = render_template('play/no_active.html')
        else:
            res['html'] = render_template('play/no_run.html')
        return res


@play_ns.route('/answer/<int:team_id>/<int:question_id>')
class TeamAnswer(Resource):
    def get(self, team_id, question_id):
        if team_id and question_id:
            answer = Answer()
            answer.load(team_id=team_id, question_id=question_id)
            if answer.answer:
                return answer.answer
        return None

    def post(self, team_id, question_id):
        data = request.form or request.get_json()
        if not db.session.query(Teams).filter_by(team_id=team_id).first():
            return {'result': None, 'error': 'No such team'}
        if not db.session.query(QuestionsAll).filter_by(question_id=question_id).first():
            return {'result': None, 'error': 'No such question'}
        if 'text' in data:
            answer = Answer()
            answer.load(team_id=team_id, question_id=question_id)
            answer.answer = data['text']
            answer.save()
            return {'result': 'OK'}
        return {'result': None}
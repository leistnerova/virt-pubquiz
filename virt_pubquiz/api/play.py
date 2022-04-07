from flask import request, render_template, session
from flask_restx import Namespace, Resource

from .. import db
from ..model import Categories, QuestionsAll, Teams
from ..utils.quiz import QuizFactory
from ..utils.run import QuizRunAdmin
from ..utils.team import Answer, TeamsList

play_ns = Namespace('play', description="Endpoint to retrieve play information")


@play_ns.route('/actual')
class PlayActual(Resource):
    def get(self):
        res = {'question_id': '-1'}
        quiz = QuizFactory().get_actual_quiz()
        run = QuizRunAdmin(quiz)
        run.load_items()
        if run.actual_item:
            if run.show_category_id:
                item = db.session.query(Categories).filter_by(category_id=run.show_category_id).first()
                item.title = item.name
                res['question_id'] = '-2'
                res['html'] = render_template('run/item.html', item=item)
            elif run.show_thanks:
                res['html'] = render_template('run/thanks.html', quiz=quiz)
            else:
                if quiz.status:
                    res['question_id'] = run.actual_item.question_id
                    res['html'] = render_template('run/item.html', item=run.actual_item, run=run, quiz=quiz)
                    if quiz.status == 'results':
                        res['answer'] = render_template('run/answer.html', item=run.actual_item)
                else:
                    res['html'] = render_template('play/no_active.html', quiz=quiz)
        else:
            res['html'] = render_template('play/no_run.html', quiz=quiz)
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


@play_ns.route('/user')
class TeamUser(Resource):
    def get(self):
        if session and session['team_user']:
            quiz = QuizFactory().get_actual_quiz()
            teams = TeamsList(quiz=quiz)
            team = teams.get_team(session['team_id'])
            return {'name': session['team_user'], 'team': team.name, 'editor': session['editor']}
        return None

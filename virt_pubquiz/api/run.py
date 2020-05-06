from datetime import datetime
from flask import request, render_template
from flask_restplus import Namespace, Resource

from .. import db
from ..model import QuestionsAll, QuizRun
from ..utils import Utils
from ..utils.run import QuizRunAdmin
from ..utils.quiz import QuizFactory

run_ns = Namespace('run', description="Endpoint to retrieve run information")


@run_ns.route('')
class Run(Resource):
    def get(self):
        run = db.session.query(QuizRun).first()
        return Utils.get_dict(run)

    def post(self):
        data = request.form or request.get_json()
        if 'next' in data and data['next'] == '1':
            run = db.session.query(QuizRun).first()
            if not run.question_next:
                return {'result': 'No next round'}
            new_run = QuizRun(question_actual=run.question_next)
            quiz = QuizFactory().get_actual_quiz()
            question_next = quiz.get_next_question(run.question_next)
            if question_next:
                new_run.question_next = question_next.question_id
            else:
                new_run.question_next = None
            new_run.question_start = None
            new_run.show_category_id = None
            db.session.delete(run)
            db.session.add(new_run)
            db.session.commit()
            return {'result': 'OK'}
        return {'result': None}


@run_ns.route('/actual')
class RunActual(Resource):
    def get(self):
        run = db.session.query(QuizRun).first()
        if run:
            item = db.session.query(QuestionsAll).filter_by(question_id=run.question_actual).first()
            item.actual = True
            return {'question_id': run.question_actual, 'html': render_template('run/item.html', item=item)}
        return None


@run_ns.route('/next')
class RunNext(Resource):
    def get(self):
        run = db.session.query(QuizRun).first()
        if run:
            item = db.session.query(QuestionsAll).filter_by(question_id=run.question_next).first()
            return {'question_id': run.question_next, 'html': render_template('run/item.html', item=item)}
        return None


@run_ns.route('/start')
class RunStart(Resource):
    def get(self):
        run = db.session.query(QuizRun).first()
        if run:
            run.question_start = datetime.now()
            db.session.commit()
            return {'result': 'OK'}
        return {'result': None}


@run_ns.route('/countdown')
class RunCountdown(Resource):
    def get(self):
        quiz = QuizFactory().get_actual_quiz()
        number = QuizRunAdmin(quiz).get_countdown()
        if number is not None:
            return {'countdown': number}
        return None


@run_ns.route('/category')
class RunCategory(Resource):
    def get(self):
        quiz = QuizFactory().get_actual_quiz()
        run = QuizRunAdmin(quiz)
        run.load_items()
        res = {'actual_category_id': run.actual_item.category_id}
        if run.next_item:
            res['next_category_id'] = run.next_item.category_id
        return res


@run_ns.route('/showcategory')
class RunShowCategory(Resource):
    def get(self):
        run = db.session.query(QuizRun).first()
        if run:
            return run.show_category_id
        return None

    def post(self):
        data = request.form or request.get_json()
        if 'type' in data and data['type']:
            quiz = QuizFactory().get_actual_quiz()
            run = QuizRunAdmin(quiz)
            run.load_items()
            if data['type'] == 'next':
                if run.next_item:
                    category_id = run.next_item.category_id
                else:
                    return {'result': None}
            else:
                category_id = run.actual_item.category_id
            run = db.session.query(QuizRun).first()
            run.show_category_id = category_id
            db.session.commit()
            return {'result': 'OK'}
        return {'result': None}

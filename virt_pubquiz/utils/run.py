from datetime import datetime

from .. import db
from ..model import Categories, QuestionsAll, QuizRun


class QuizRunAdmin:
    quiz = None
    actual_item = None
    next_item = None
    show_category_id = None
    question_start = None

    def __init__(self, quiz):
        self.quiz = quiz

    def init_run(self):
        db.session.query(QuizRun).delete()
        item_actual = self.quiz.get_next_question()
        run = QuizRun()
        if item_actual:
            run.question_actual = item_actual.question_id,
            item_next = self.quiz.get_next_question(item_actual.question_id)
            if item_next:
                run.question_next = item_next.question_id,
            db.session.add(run)
            db.session.commit()

    def load_items(self):
        run = db.session.query(QuizRun).first()
        if not run:
            self.init_run()
        run = db.session.query(QuizRun).first()
        self.actual_item = db.session.query(QuestionsAll).filter_by(question_id=run.question_actual).first()
        self.actual_item.actual = True
        if run.question_next:
            self.next_item = db.session.query(QuestionsAll).filter_by(question_id=run.question_next).first()
        self.question_start = run.question_start
        self.show_category_id = run.show_category_id

    def get_countdown(self):
        run = db.session.query(QuizRun).first()
        if run and run.question_start:
            item = db.session.query(QuestionsAll).filter_by(question_id=run.question_actual).first()
            diff =  datetime.now() - run.question_start
            number = diff.seconds - item.time_limit
            if number < 0:
                return number * -1
            else:
                return 0
        return None

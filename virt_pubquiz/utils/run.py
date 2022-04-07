from datetime import datetime

from .. import db
from ..model import Categories, QuestionsAll, QuizRun, QuizRunDone


class QuizRunAdmin:
    quiz = None
    actual_item = None
    next_item = None
    show_category_id = None
    show_thanks = None
    question_start = None
    questions_done = 0

    def __init__(self, quiz):
        self.quiz = quiz

    def init_run(self):
        db.session.query(QuizRunDone).delete()
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

    def delete_run(self):
        db.session.query(QuizRunDone).delete()
        db.session.query(QuizRun).delete()
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
        self.show_thanks = run.show_thanks
        self.questions_done = db.session.query(QuizRunDone).count()

    def get_countdown(self):
        run = db.session.query(QuizRun).first()
        if run and run.question_start:
            item = db.session.query(QuestionsAll).filter_by(question_id=run.question_actual).first()
            diff = datetime.now() - run.question_start
            number = diff.seconds - item.time_limit
            if number < 0:
                return number * -1
            else:
                return 0
        return None

    def get_category(self):
        cat_id = self.show_category_id if self.show_category_id else self.actual_item.category_id
        item = db.session.query(Categories).filter_by(category_id=cat_id).first()
        item.title = item.name
        item.actual = True
        return item

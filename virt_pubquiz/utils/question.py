import sys

from ..model import Questions
from .. import db
from . import Utils


class QuestionFactory:
    def get_question(self, question_type):
        class_name = 'Question' + question_type[:1].upper() + question_type[1:]
        cls = getattr(sys.modules[__name__], class_name)
        return cls()


class QuestionBase:
    _model = Questions
    _name = None
    question_id = None
    question_type = None
    task = None

    def get_db_obj(self):
        res = self._model()
        Utils.set_vars(res, self)
        return res


class QuestionOpen(QuestionBase):
    title = None
    time_limit = None
    picture = None
    answer_picture = None

    def __init__(self):
        self.question_type = 'open'

    def load(self):
        """
        Load question from database
        """
        if (self.question_id):
            question = db.session.query(self._model).filter_by(question_id=self.question_id).first()
            self.__dict__.update(question.__dict__)

    def save(self):
        """ Save question in database """
        if self.question_id:
            question = db.session.query(self._model).filter_by(question_id=self.question_id).first()
            Utils.set_vars(question, self)
        else:
            db_obj = self.get_db_obj()
            db.session.add(db_obj)
            db.session.flush()
            db.session.refresh(db_obj)
            self.question_id = db_obj.question_id
        db.session.commit()

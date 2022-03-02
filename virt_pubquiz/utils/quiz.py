from os import listdir, mkdir
from os.path import isdir, isfile, join
import shutil
import sys

from flask import current_app as app
import yaml

from ..model import (
    Categories, CategoryQuestion, QuestionsAll,
    Questions, Quizes
)
from .. import db
from . import Utils
from .question import QuestionFactory


class QuizFactory:

    def get_quiz(self, quiz_type):
        class_name = 'Quiz' + quiz_type[:1].upper() + quiz_type[1:]
        cls = getattr(sys.modules[__name__], class_name)
        return cls()

    def get_quiz_from_dir(self, from_dir, new_update='new'):
        quiz_def = QuizImport().get_quiz_def(from_dir)
        quiz = self.get_quiz(quiz_def['type']['name'])
        quiz.import_from_dir(from_dir, new_update, quiz_def)
        return quiz

    def get_actual_quiz(self, full=False):
        res = db.session.query(Quizes.quiz_type).order_by(Quizes.quiz_id.desc()).first()
        if res:
            quiz = self.get_quiz(res.quiz_type)
            quiz.load(full=full)
        else:
            quiz = QuizBase()
        return quiz


class QuizImport:
    """
    Class used by importing quiz from github repo directory
    """
    import_dir = ''
    questions_dir = 'questions'
    pictures_dir = 'pictures'
    app_files_dir = ''

    def __init__(self):
        with app.app_context():
            self.import_dir = app.config['IMPORT_DIR']
            self.app_files_dir = join(app.root_path, app.config['FILES_DIR'])

    def get_dirs(self):
        """
        Get all github directories from import directory

        Returns:
            list: directory names
        """
        result = []
        for f in listdir(self.import_dir):
            if isdir(join(self.import_dir, f)) and isdir(join(self.import_dir, f, '.git')):
                result.append(f)
        result.sort()
        return result

    def get_quiz_def(self, from_dir):
        """
        Get definition in quiz.yaml from github repo directory

        Args:
            from_dir (str): github repo directory
        Returns:
            dict: quiz definition
        """
        from_dir = join(self.import_dir, from_dir)
        with open(join(from_dir, 'quiz.yaml'), 'r') as stream:
            return yaml.safe_load(stream)
        return {}

    def get_question_def(self, from_dir, file_name):
        """
        Get definition in question yaml from github repo directory

        Args:
            from_dir (str): github repo directory
            file_name (str): name of the question file
        Returns:
            dict: question definition
        """
        from_dir = join(self.import_dir, from_dir, self.questions_dir)
        try:
            with open(join(from_dir, file_name), 'r') as stream:
                return yaml.safe_load(stream)
        except Exception as ex:
            app.logger.error(str(ex))
        return {}

    def import_file(self, from_dir, file_name, subdir):
        path_from = join(self.import_dir, from_dir, self.pictures_dir, file_name)
        if isfile(path_from):
            path_to = join(self.app_files_dir, subdir)
            if not isdir(path_to):
                mkdir(path_to)
            shutil.copyfile(path_from, join(path_to, file_name))


class QuizBase:
    _model = Quizes
    quiz_id = None
    quiz_type = None
    categories = []
    categories_count = 0
    questions = []
    questions_count = 0
    from_dir = None
    status = None
    individual = 0

    def get_db_obj(self):
        res = self._model()
        Utils.set_vars(res, self)
        return res


class QuizDefault(QuizBase):
    title = None
    time_limit = None
    random_order = 0

    def __init__(self):
        self.quiz_type = 'default'
        self.categories = []
        self.categories_count = 0
        self.questions = []
        self.questions_count = 0

    def load(self, full=False):
        """
        Load quiz from database

        Args:
            full (boolean): True - load also categories and questions, False - only main attributes
        """
        if (self.quiz_id):
            quiz = db.session.query(self._model).filter_by(quiz_id=self.quiz_id).first()
        else:
            quiz = db.session.query(self._model).order_by(self._model.quiz_id.desc()).first()
        self.__dict__.update(quiz.__dict__)
        if full:
            self.load_questions()
            self.questions_count = len(self.questions)
            self.categories_count = self.categories.count()
        else:
            self.categories_count = db.session.query(Categories).filter_by(quiz_id=self.quiz_id).count()
            self.questions_count = db.session.query(QuestionsAll).filter_by(quiz_id=self.quiz_id).count()

    def load_questions(self):
        """
        Load quiz questions and categories from database
        """
        self.questions = []
        self.categories = []
        if self.quiz_id:
            self.categories = db.session.query(Categories).filter_by(quiz_id=self.quiz_id)
            number = 1
            qs = db.session.query(QuestionsAll).filter_by(quiz_id=self.quiz_id).order_by(
                QuestionsAll.category_id, QuestionsAll.question_id
            )
            for question in qs:
                question.number = number
                self.questions.append(question)
                number += 1

    def import_from_dir(self, from_dir, new_update='new', quiz_def=None):
        """
        Load quiz attributes from github repo directory

        Args:
            from_dir (str): github repo directory
            new_update (str): new - load as new quiz, update - load last quiz from database and update attributes
        """
        if (from_dir):
            self.from_dir = from_dir
            import_obj = QuizImport()
            if new_update != 'new':
                self.load()
            # update attributes from yaml
            if not quiz_def:
                quiz_def = import_obj.get_quiz_def(from_dir)
            self.title = quiz_def['title']
            self.time_limit = quiz_def['time_limit']
            self.random_order = int(quiz_def['type']['options']['random_order'])
            if 'individual' in quiz_def['type']['options']:
                self.individual = int(quiz_def['type']['options']['individual'])

            # get categories and questions
            self.categories = []
            self.questions = []
            for category in quiz_def['type']['options']['categories']:
                cc = Categories(name=category['name'])
                if 'picture' in category:
                    cc.picture = category['picture']
                cc._questions = category['questions']
                self.categories.append(cc)
                if 'questions' in category and category['questions']:
                    for question_file in category['questions']:
                        question_def = import_obj.get_question_def(from_dir, question_file)
                        if question_def:
                            question = QuestionFactory().get_question(question_def['type']['name'])
                            question._file = question_file
                            question.task = self.parse_text(question_def['task'])
                            question.answer = question_def['answer']
                            for i in ('title', 'picture', 'answer_picture', 'time_limit'):
                                if i in question_def:
                                    setattr(question, i, question_def[i])
                            self.questions.append(question)
                        else:
                            app.logger.error('{} not loaded'.format(question_file))

        return True

    def save(self, full=False):
        """
        Save quiz in database

        Args:
            full (boolean): True - save also categories and questions, False - only main attributes
        """
        is_update = self.quiz_id
        if is_update:
            quiz = db.session.query(self._model).filter_by(quiz_id=self.quiz_id).first()
            Utils.set_vars(quiz, self)
        else:
            db_obj = self.get_db_obj()
            db.session.add(db_obj)
            db.session.flush()
            db.session.refresh(db_obj)
            self.quiz_id = db_obj.quiz_id
        db.session.commit()

        if full:
            import_obj = QuizImport()
            # questions
            if is_update:
                db.session.query(Questions).filter_by(quiz_id=self.quiz_id).delete()
            for question in self.questions:
                question.quiz_id = self.quiz_id
                question.save()
                if question.picture:
                    import_obj.import_file(self.from_dir, question.picture, str(self.quiz_id))
                if question.answer_picture:
                    import_obj.import_file(self.from_dir, question.answer_picture, str(self.quiz_id))

            # categories
            if is_update:
                db.session.query(Categories).filter_by(quiz_id=self.quiz_id).delete()
            for category in self.categories:
                if is_update:
                    db.session.query(CategoryQuestion).filter_by(category_id=category.category_id).delete()
                category.quiz_id = self.quiz_id
                db.session.add(category)
                db.session.flush()
                if category.picture:
                    import_obj.import_file(self.from_dir, category.picture, str(self.quiz_id))
                if category._questions:
                    for question in self.questions:
                        if question._file in category._questions:
                            db.session.add(CategoryQuestion(
                                question_id=question.question_id,
                                category_id=category.category_id
                            ))

        db.session.commit()

    def get_next_question(self, question_id=None):
        if question_id:
            res = db.session.query(QuestionsAll).filter(
                QuestionsAll.quiz_id == self.quiz_id, QuestionsAll.question_id > question_id
            ).order_by(QuestionsAll.question_id.asc()).first()
        else:
            qq = db.session.query(QuestionsAll).filter_by(quiz_id=self.quiz_id).order_by(QuestionsAll.question_id.asc())
            res = qq.first()
        return res

    def get_next_category(self, question_id=None):
        question = self.get_next_question(question_id)
        if question.category_id:
            return db.session.query(Categories).filter_by(category_id=question.category_id).first()
        return None

    def parse_text(self, text):
        return text.replace('\n', '<br>')

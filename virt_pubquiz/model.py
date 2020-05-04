from . import db
from flask_login import current_user


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    is_active = db.Column(db.Integer)

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        if self.name == current_user.name:
            return True
        else:
            return False


class Quizes(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    quiz_type = db.Column(db.String(50), nullable=False)
    random_order = db.Column(db.Integer)
    time_limit = db.Column(db.Integer)
    is_active = db.Column(db.Integer, default=0)
    from_dir = db.Column(db.String(256))


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    picture = db.Column(db.String(256))


class Questions(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(50), nullable=False)
    quiz_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(256))
    picture = db.Column(db.String(256))
    task = db.Column(db.Text)
    time_limit = db.Column(db.Integer)


class QuestionsAll(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    question_type = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(256))
    task = db.Column(db.Text)
    time_limit = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    category = db.Column(db.String(256))
    quiz_id = db.Column(db.Integer, nullable=False)


class CategoryQuestion(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, primary_key=True)


class QuizRun(db.Model):
    run_id = db.Column(db.Integer, primary_key=True)
    question_actual = db.Column(db.Integer, nullable=False)
    question_next = db.Column(db.Integer, nullable=False)
    question_start = db.Column(db.Date)
    show_category_id = db.Column(db.Integer)


class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)


class TeamUsers(db.Model):
    team_user_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    editor = db.Column(db.Integer)


class TeamAnswers(db.Model):
    team_id = db.Column(db.Integer, nullable=False, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False, primary_key=True)
    answer = db.Column(db.Text)
    points = db.Column(db.Integer)

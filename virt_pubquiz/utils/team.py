from .. import db
from ..model import Teams, TeamAnswers, TeamAnswersAll, TeamUsers
from . import Utils
from .quiz import QuizFactory


class TeamsList:
    quiz_id = None
    teams = []

    def __init__(self, quiz=None, full=False):
        if not quiz:
            quiz = QuizFactory().get_actual_quiz()
        self.quiz_id = quiz.quiz_id
        self.teams = []
        if self.quiz_id:
            for team in db.session.query(Teams).filter_by(quiz_id=self.quiz_id).order_by(Teams.name):
                team = Team(team_id=team.team_id, quiz_id=self.quiz_id, name=team.name)
                if full:
                    team.load_users()
                self.teams.append(team)

    def get_team(self, team_id):
        for team in self.teams:
            if team.team_id == int(team_id):
                return team
        return None


class Team:
    team_id = None
    quiz_id = None
    name = None
    editor = None
    users = []
    users_str = ''
    answers = []
    points = 0

    def __init__(self, quiz_id=None, name=None, team_id=None):
        self.team_id = team_id
        self.quiz_id = quiz_id
        self.name = name
        self.users = []
        self.users_str = ''
        self.answers = []
        self.points = 0
        if (team_id):
            team = db.session.query(Teams).filter_by(team_id=team_id).first()
            self.name = team.name

    def load_users(self):
        self.users = []
        if self.team_id:
            for user in db.session.query(TeamUsers).filter_by(team_id=self.team_id):
                if user.editor:
                    self.editor = user.name
                self.users.append(user.name)
            self.users_str = ', '.join(self.users)

    def save(self):
        if self.team_id:
            team = db.session.query(Teams).filter_by(team_id=self.team_id).first()
            team.name = self.name
        else:
            team = Teams(quiz_id=self.quiz_id, name=self.name)
            db.session.add(team)
            db.session.flush()
            db.session.refresh(team)
            self.team_id = team.team_id
        db.session.commit()

    def get_users(self):
        return ', '.join(self.users)

    def load_answers(self):
        self.answers = []
        if self.team_id:
            ans = db.session.query(TeamAnswersAll).filter_by(team_id=self.team_id).order_by(TeamAnswersAll.question_id)
            for answer in ans:
                new_answer = Answer()
                Utils.set_vars(new_answer, answer)
                self.answers.append(new_answer)
                if answer.points:
                    self.points += answer.points


class TeamUser:
    team_user_id = None
    team_id = None
    name = None
    editor = None

    def load(self, user_name, team_id, editor=None):
        user = db.session.query(TeamUsers).filter_by(name=user_name, team_id=team_id).first()
        if user:
            Utils.set_vars(self, user)
        else:
            self.name = user_name
            self.team_id = team_id
            self.editor = editor

    def save(self):
        if self.team_user_id:
            user = db.session.query(TeamUsers).filter_by(team_user_id=self.team_user_id).first()
            Utils.set_vars(user, self)
        else:
            user = TeamUsers()
            Utils.set_vars(user, self)
            db.session.add(user)
        db.session.commit()


class Answer:
    question_id = None
    team_id = None
    answer = None
    points = None

    def load(self, team_id, question_id):
        answer = db.session.query(TeamAnswers).filter_by(question_id=question_id, team_id=team_id).first()
        if answer:
            Utils.set_vars(self, answer)
        else:
            self.team_id = team_id
            self.question_id = question_id

    def save(self):
        answer = db.session.query(TeamAnswers).filter_by(question_id=self.question_id, team_id=self.team_id).first()
        if answer:
            answer.answer = self.answer
            answer.points = self.points
        else:
            answer = TeamAnswers()
            Utils.set_vars(answer, self)
            db.session.add(answer)
        db.session.commit()

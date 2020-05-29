from flask import Blueprint
from flask import render_template, request
from flask_login import login_required

from .utils.quiz import QuizFactory
from .utils.team import TeamsList, Team

team = Blueprint('team', __name__)


@team.route('/teams', methods=['POST', 'GET'])
@login_required
def list():
    if request.method == 'POST' and request.form['name']:
        teams_list = TeamsList()
        team_name = request.form['name'].strip()
        team_exist = False
        for team in teams_list.teams:
            if team.name == team_name:
                team_exist = True
        if not team_exist:
            quiz = QuizFactory().get_actual_quiz(full=True)
            if quiz:
                team = Team(quiz_id=quiz.quiz_id, name=team_name)
                team.save()
    teams_list = TeamsList(full=True)
    return render_template(
        'teams.html',
        teams=teams_list.teams
    )

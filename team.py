from flask import current_app as app
from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from .utils.quiz import QuizFactory
from .utils.team import TeamsList, Team

team = Blueprint('team', __name__)


@team.route('/teams', methods=['POST', 'GET'])
@login_required
def list():
    if request.method == 'POST':
        quiz = QuizFactory().get_actual_quiz(full=True)
        if quiz:
            team = Team(quiz_id=quiz.quiz_id, name=request.form['name'])
            team.save()
    teams_list = TeamsList(full=True)
    return render_template(
        'teams.html',
        teams=teams_list.teams
    )

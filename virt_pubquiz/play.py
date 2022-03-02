from flask import Blueprint
from flask import redirect, request, render_template, session, url_for

from .utils.quiz import QuizFactory
from .utils.team import TeamsList, TeamUser

play = Blueprint('play', __name__)


@play.route('/play', methods=['POST', 'GET'])
def index():
    quiz = QuizFactory().get_actual_quiz()
    teams = TeamsList(quiz=quiz, full=True)
    if request.method == 'POST' and (quiz.individual or request.form['name']):
        if quiz.individual:
            editor = 1
            team = teams.get_team(request.form['team_id'])
            user_name = team.name
        else:
            editor = 1 if 'editor' in request.form else 0
            user_name = request.form['name']
        user = TeamUser()
        user.load(
            user_name=user_name, team_id=request.form['team_id'], editor=editor
        )
        user.save()
        session['team_user'] = user.name
        session['team_id'] = user.team_id
        session['editor'] = user.editor

    if 'team_user' not in session or not session['team_user']:
        return render_template(
            'play/login.html', quiz_name=quiz.title, teams=teams.teams, individual=quiz.individual
        )

    return render_template(
        'play/play.html',
        team=teams.get_team(session['team_id']), individual=quiz.individual
    )


@play.route('/stop', methods=['POST', 'GET'])
def stop():
    session['team_user'] = None
    session['team_id'] = None
    session['editor'] = None
    return redirect(url_for('play.index'))

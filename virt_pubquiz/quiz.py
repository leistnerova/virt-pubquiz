from flask import current_app as app
from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from .utils.quiz import QuizFactory, QuizImport
from .utils.run import QuizRunAdmin
from .utils.team import Team, TeamsList

quiz = Blueprint('quiz', __name__)


@quiz.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        quiz = QuizFactory().get_actual_quiz()
        is_active = request.form.get('is_active', 0)
        if quiz.is_active == 1 and not is_active:
            run = QuizRunAdmin(quiz)
            run.init_run()
        quiz.title = request.form['title']
        quiz.time_limit = request.form['time_limit']
        quiz.is_active = is_active
        quiz.save()
        flash('Quiz attributes were updated.')
    quiz = QuizFactory().get_actual_quiz(full=True)
    import_dirs = QuizImport().get_dirs()
    return render_template(
        'quiz_settings.html',
        quiz=quiz,
        directories=import_dirs
    )


@quiz.route('/import_quiz', methods=['POST'])
@login_required
def import_quiz():
    quiz = QuizFactory().get_quiz_from_dir(
        from_dir=request.form['from_dir'],
        new_update=request.form['new_update']
    )
    quiz.save(full=True)
    app.logger.info('Quiz %s imported'.format(quiz.quiz_id))
    flash('Quiz was imported')
    return redirect(url_for('quiz.settings'))


@quiz.route('/run_quiz', methods=['POST', 'GET'])
@login_required
def run():
    quiz = QuizFactory().get_actual_quiz()
    run = QuizRunAdmin(quiz)
    if request.method == 'POST' and request.form.get('reload', 0):
        run.init_run()
        app.logger.info('Run was reloader')
    run.load_items()
    if quiz.is_active:
        return render_template(
            'run/admin.html',
            actual_item=run.actual_item,
            next_item=run.next_item,
            show_category_id=run.show_category_id
        )
    else:
        category = quiz.get_next_category()
        category.title = category.name
        return render_template(
            'run/init.html',
            quiz=quiz,
            category=category,
            show_category_id=run.show_category_id
        )


@quiz.route('/activate_quiz', methods=['POST'])
@login_required
def activate():
    quiz = QuizFactory().get_actual_quiz()
    quiz.is_active = 1
    quiz.save()
    run = QuizRunAdmin(quiz)
    run.init_run()
    return redirect(url_for('quiz.run'))


@quiz.route('/results', methods=['POST', 'GET'])
@login_required
def results():
    teams_list = TeamsList()
    if request.method == 'POST':
        team_active = int(request.form['team_id'])
        tt = Team(team_id=team_active)
        tt.load_answers()
        for answer in tt.answers:
            answer.points = request.form['answer_' + str(answer.question_id) + '_points']
            app.logger.info(answer)
            answer.save()
        flash('Results for {} were saved'.format(tt.name))
    else:
        team_active = teams_list.teams[0].team_id
    for team in teams_list.teams:
        team.load_answers()
    return render_template(
        'result/eval.html',
        teams=teams_list.teams,
        team_active=team_active
    )

from flask import current_app as app
from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from .utils.quiz import QuizFactory, QuizImport
from .utils.run import QuizRunAdmin
from .utils.team import TeamsList

quiz = Blueprint('quiz', __name__)


@quiz.route('/settings', methods=['POST', 'GET'])
@login_required
def settings():
    if request.method == 'POST':
        quiz = QuizFactory().get_actual_quiz()
        status = 'active' if request.form.get('is_active', 0) else ''
        if quiz.status and not status:
            run = QuizRunAdmin(quiz)
            run.init_run()
        quiz.title = request.form['title']
        quiz.time_limit = request.form['time_limit']
        if not quiz.status or not status:  # do not rewrite existing status to 'active'
            quiz.status = status
        app.logger.info(quiz.status)
        quiz.save()
        flash('Quiz attributes were updated.', 'success')
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
    app.logger.info('Quiz {} imported'.format(quiz.quiz_id))
    flash('Quiz was imported', 'success')
    return redirect(url_for('quiz.settings'))


@quiz.route('/run_quiz', methods=['POST', 'GET'])
@login_required
def run():
    quiz = QuizFactory().get_actual_quiz()
    run = QuizRunAdmin(quiz)
    if request.method == 'POST':
        if request.form.get('results', 0):
            run.init_run()
            quiz.status = 'results'
            quiz.save()
            app.logger.info('Moved to results')
        if request.form.get('deactivate', 0):
            run.delete_run()
            quiz.status = ''
            quiz.save()
            run = QuizRunAdmin(quiz)
            app.logger.info('Quiz deactivated')
    run.load_items()
    if quiz.status != '':
        if run.show_category_id:
            item = run.get_category()
        else:
            item = run.actual_item
        return render_template(
            'run/admin.html',
            quiz=quiz,
            run=run,
            actual_item=item,
            next_item=run.next_item,
            show_category_id=run.show_category_id
        )
    else:
        category = quiz.get_next_category()
        category.title = category.name
        return render_template(
            'run/init.html',
            category=category,
            show_category_id=run.show_category_id
        )


@quiz.route('/activate_quiz', methods=['POST'])
@login_required
def activate():
    quiz = QuizFactory().get_actual_quiz()
    quiz.status = 'active'
    quiz.save()
    run = QuizRunAdmin(quiz)
    run.delete_run()
    return redirect(url_for('quiz.run'))


@quiz.route('/deactivate_quiz', methods=['POST'])
@login_required
def deactivate():
    return redirect(url_for('quiz.run'))


@quiz.route('/results')
@login_required
def results():
    teams_list = TeamsList()
    for team in teams_list.teams:
        team.load_answers()
    return render_template(
        'result/eval.html',
        teams=teams_list.teams,
        team_active=teams_list.teams[0].team_id
    )

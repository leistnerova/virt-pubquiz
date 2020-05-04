from os.path import isfile, join

from flask import current_app as app
from flask import Blueprint
from flask import abort, render_template, send_file
from flask_login import current_user

from .utils.quiz import QuizFactory


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/file/<name>')
def get_file(name):
    quiz = QuizFactory().get_actual_quiz()
    path_file = join(app.root_path, app.config['FILES_DIR'], str(quiz.quiz_id), name)
    if not isfile(path_file):
        abort(404)
    return send_file(path_file)

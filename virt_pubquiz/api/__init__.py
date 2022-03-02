from flask import Blueprint
from flask_restx import Api

from .categories import categories_ns
from .questions import questions_ns
from .teams import teams_ns
from .run import run_ns
from .play import play_ns


api = Blueprint('api', __name__, url_prefix='/api')
quiz_api = Api(api)

quiz_api.add_namespace(questions_ns, '/questions')
quiz_api.add_namespace(categories_ns, '/categories')
quiz_api.add_namespace(teams_ns, '/teams')
quiz_api.add_namespace(run_ns, '/run')
quiz_api.add_namespace(play_ns, '/play')

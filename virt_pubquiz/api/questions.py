from flask_restx import Namespace, Resource

from .. import db
from ..model import Questions
from ..utils import Utils

questions_ns = Namespace('questions', description="Endpoint to retrieve questions")


@questions_ns.route('/<int:question_id>')
class Question(Resource):
    def get(self, question_id):
        question = db.session.query(Questions).filter_by(question_id=question_id).first()
        return Utils.get_dict(question)

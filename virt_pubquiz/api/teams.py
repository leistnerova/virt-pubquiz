import sys

from flask import current_app as app
from flask import request
from flask_restx import Namespace, Resource

from ..utils.team import Answer, Team

teams_ns = Namespace('teams', description="Endpoint to retrieve team information")


@teams_ns.route('/<int:team_id>/members')
class TeamMembers(Resource):
    def get(self, team_id):
        team = Team(team_id=team_id)
        team.load_users()
        return team.users_str


@teams_ns.route('/<int:team_id>/points')
class TeamPoints(Resource):
    def get(self, team_id):
        team = Team(team_id=team_id)
        team.load_answers()
        return team.points


@teams_ns.route('/<int:team_id>/answers/<int:question_id>/points')
class TeamAnswers(Resource):
    def post(self, team_id, question_id):
        data = request.form or request.get_json()
        if 'points' in data:
            try:
                answer = Answer()
                answer.load(team_id=team_id, question_id=question_id)
                answer.points = int(data['points'])
                answer.save()
                return {'result': 'OK'}
            except Exception:
                app.logger.error(sys.exc_info()[1])
                return {'result': None, 'error': 'Error saving points'}
        return {'result': None}

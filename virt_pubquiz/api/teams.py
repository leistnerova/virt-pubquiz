from flask_restplus import Namespace, Resource

from ..utils.team import Team

teams_ns = Namespace('teams', description="Endpoint to retrieve team information")


@teams_ns.route('/<int:team_id>/members')
class TeamMembers(Resource):
    def get(self, team_id):
        team = Team(team_id=team_id)
        team.load_users()
        return team.users_str

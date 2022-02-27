from flask_restx import Namespace, Resource

from .. import db
from ..model import Categories
from ..utils import Utils

categories_ns = Namespace('categories', description="Endpoint to retrieve categories")


@categories_ns.route('/<int:category_id>')
class Category(Resource):
    def get(self, category_id):
        category = db.session.query(Categories).filter_by(category_id=category_id)
        return Utils.get_dict(category)

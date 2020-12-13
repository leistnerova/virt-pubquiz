from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# sys.path.append(os.path.split(__file__)[0])
db = SQLAlchemy()


def create_app():
    app = Flask(
        __name__, template_folder="themes/templates",
        static_folder="themes/static"
    )

    app.config.from_pyfile(".config/config.cfg")

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .quiz import quiz as quiz_blueprint
    app.register_blueprint(quiz_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .team import team as team_blueprint
    app.register_blueprint(team_blueprint)

    from .play import play as play_blueprint
    app.register_blueprint(play_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .model import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @app.context_processor
    def get_background_file():
        return {'background_file': app.config['BACKGROUND_FILE']}

    return app

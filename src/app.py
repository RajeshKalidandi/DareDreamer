from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from src.config import Config
import json

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from src.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from src.routes import bp
    app.register_blueprint(bp)

    # Add custom filter
    @app.template_filter('json_loads')
    def json_loads_filter(s):
        return json.loads(s) if s else []

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
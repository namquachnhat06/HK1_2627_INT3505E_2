import os
from flask import Flask
from .extensions import db, migrate
from .api.products import products_bp
from .api.orders import orders_bp
from .api.health import health_bp
from .api.errors import register_error_handlers
from .config import DefaultConfig

def create_app(config=None):
    cfg = config or os.environ.get("APP_CONFIG", DefaultConfig)
    app = Flask(__name__)
    app.config.from_object(cfg)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)

    register_error_handlers(app)
    return app
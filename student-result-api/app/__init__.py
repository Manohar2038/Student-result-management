from flask import Flask
import pymysql
import pymysql.cursors
from config import Config

connection = None

def get_db():
    global connection
    if connection is None or not connection.open:
        cfg = Config()
        connection = pymysql.connect(
            host     = Config.MYSQL_HOST,
            user     = Config.MYSQL_USER,
            password = Config.MYSQL_PASSWORD,
            database = Config.MYSQL_DATABASE,
            cursorclass = pymysql.cursors.DictCursor
        )
    return connection

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.students import students_bp
    from app.routes.reports  import reports_bp

    app.register_blueprint(students_bp, url_prefix='/api/v1')
    app.register_blueprint(reports_bp,  url_prefix='/api/v1')

    return app
from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = MySQL()
bcrypt = Bcrypt()
jwt = JWTManager()
# app = Flask()
app = Flask(__name__)

def create_app():
    cors = CORS(app, resources=r'/*')
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'absensi_karyawan'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    app.config["JWT_SECRET_KEY"] = 'secret'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # karyawan
    from API.Karyawan.Karyawan import karyawan
    app.register_blueprint(karyawan)

    # activity
    from API.Activity.Activity import activity
    app.register_blueprint(activity)

    # absensi
    from API.Absensi.Absensi import absensi
    app.register_blueprint(absensi)

    return app
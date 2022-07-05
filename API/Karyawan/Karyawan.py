from flask import Flask, render_template, Blueprint
from flask import jsonify, request
from flask_jwt_extended import create_access_token
import flask_praetorian
from ..run import db, jwt, bcrypt

karyawan = Blueprint('karyawan',__name__)
guard = flask_praetorian.Praetorian()

@karyawan.route('/karyawan/register', methods=['POST'])
def register_karyawan():
    cur = db.connection.cursor()

    nama_karyawan = request.get_json()['nama_karyawan']
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')

    cur.execute("INSERT INTO karyawan (id_karyawan,nama_karyawan,username,email,password) "
                " SELECT MAX(id_karyawan)+1, "
                "'" + str(nama_karyawan) + "', "
                "'" + str(username) + "', "
                "'" + str(email) + "', "
                "'" + str(password) + "' " +
                "FROM karyawan")

    db.connection.commit()
    result = \
        {
            'nama_karyawan': nama_karyawan,
            'username': username,
            'email' : email,
            'password': password
        }

    return jsonify({"result":result})

# LOGIN
@karyawan.route('/karyawan/login', methods=['POST'])
def login():
    cur = db.connection.cursor()
    username = request.get_json()['username']
    password = request.get_json()['password']


    cur.execute("SELECT * FROM karyawan where username = '" + str(username) + "'")
    rv = cur.fetchone()

    if bcrypt.check_password_hash(rv['password'], password):
        access_token = create_access_token(
            identity={'id_karyawan': rv['id_karyawan'],
                      'username': rv['username'],
                      'email': rv['email'],
                      'nama_karyawan': rv['nama_karyawan']})
        result = jsonify({"result": access_token})

    else:
        result = jsonify({"error": "Invalid username and password"})

    return result
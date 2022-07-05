from flask import Flask, render_template, Blueprint
from flask import jsonify, request
from flask_jwt_extended import create_access_token
import flask_praetorian
from ..run import db, jwt, bcrypt
from datetime import date, datetime

absensi = Blueprint('absensi',__name__)
guard = flask_praetorian.Praetorian()
today = date.today()
now = datetime.now()

@absensi.route('/absensi', methods=['POST'])
def create_activity():
    cur = db.connection.cursor()

    id_karyawan = request.get_json()['id_karyawan']
    tanggal_absensi = today.strftime("%B %d, %Y")
    check_in = now.strftime("%H:%M:%S")
    check_out = now.strftime("%H:%M:%S")

    cur.execute("INSERT INTO absensi (id_absensi,id_karyawan) "
                " SELECT MAX(id_absensi)+1, "
                "'" + str(id_karyawan) + "'"
                "FROM absensi")

    db.connection.commit()

    return jsonify({"Result": "Check in Successfully"})

# Get Check in
@absensi.route('/absensi', methods=['GET'])
def get_all_absensi():
    cur = db.connection.cursor()
    cur.execute("SELECT nama_karyawan, tanggal_absensi, check_in, check_out "
                "FROM absensi as abs "
                "INNER JOIN karyawan as k "
                "ON abs.id_karyawan = k.id_karyawan")
    rv = cur.fetchall()
    return jsonify(rv)

# UPDATE
@absensi.route('/absensi/<id_absensi>', methods=['PUT'])
def update_check_out(id_absensi):
    cur = db.connection.cursor()

    check_out = str(now)

    cur.execute("UPDATE absensi SET check_out = '"+ check_out + "'"
                             + "WHERE id_absensi =" + id_absensi)

    db.connection.commit()

    return jsonify({"Result": "Check out Successfully"})

# GET check out
@absensi.route('/absensi', methods=['GET'])
def get_all_check_out():
    cur = db.connection.cursor()
    cur.execute("SELECT nama_karyawan, tanggal_absensi, check_out "
                "FROM absensi as abs "
                "INNER JOIN karyawan as k "
                "ON abs.id_karyawan = k.id_karyawan")
    rv = cur.fetchall()
    return jsonify(rv)
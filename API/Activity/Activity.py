from flask import Flask, render_template, Blueprint
from flask import jsonify, request
import flask_praetorian
from ..run import db, jwt, bcrypt
from datetime import date, datetime

activity = Blueprint('activity',__name__)
guard = flask_praetorian.Praetorian()
today = date.today()
now = datetime.now()

@activity.route('/activity', methods=['POST'])
def create_activity():
    cur = db.connection.cursor()

    id_karyawan = request.get_json()['id_karyawan']
    activity = request.get_json()['activity']
    tanggal_activity = str(now)

    cur.execute("INSERT INTO activity (id_activity,id_karyawan,activity, tanggal_activity) "
                " SELECT MAX(id_activity)+1, "
                "'" + str(id_karyawan) + "', "
                "'" + str(activity) + "', "                                         
                "'" + tanggal_activity + "' " +
                "FROM activity")

    db.connection.commit()
    result = \
        {
            'id_karyawan': id_karyawan,
            'activity' : activity,
            'tanggal_activity' : tanggal_activity
        }

    return jsonify({"result":result})

# READ
@activity.route('/activity', methods=['GET'])
def get_all_activity():
    cur = db.connection.cursor()
    cur.execute("SELECT nama_karyawan, activity "
                "FROM activity as a "
                "INNER JOIN karyawan as k "
                "ON a.id_karyawan = k.id_karyawan")
    rv = cur.fetchall()
    return jsonify(rv)

@activity.route('/activity/date', methods=['GET'])
def get_activity_by_date():
    cur = db.connection.cursor()
    cur.execute("SELECT nama_karyawan, activity, tanggal_activity "
                "FROM activity as a "
                "INNER JOIN karyawan as k "
                "ON a.id_karyawan = k.id_karyawan "
                "ORDER BY tanggal_activity")
    rv = cur.fetchall()
    return jsonify(rv)

# UPDATE
@activity.route('/activity/<id_activity>', methods=['PUT'])
def update_activity(id_activity):
    cur = db.connection.cursor()

    activity = request.get_json()['activity']

    cur.execute("UPDATE activity SET activity = '"+ str(activity) + "'"
                             + "WHERE id_activity =" + id_activity)

    db.connection.commit()

    result = \
        {
            'activity': activity
        }

    return jsonify({"result":result})

# DELETE
@activity.route('/activity/<id_activity>', methods=['DELETE'])
def delete_activity(id_activity):
    cur = db.connection.cursor()
    response = cur.execute("DELETE FROM activity where id_activity=" + id_activity)
    db.connection.commit()

    if response> 0:
        result = {'message' : 'record deleted'}
    else:
        result = {'message' : 'no record found'}
    return jsonify({"result": result})
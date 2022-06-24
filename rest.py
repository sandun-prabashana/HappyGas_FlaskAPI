from colorama import Cursor
import pymysql
from sqlalchemy import true
from app import app
from db import mysql
from flask import request, jsonify
import jwt
import random
from flask import flash, request
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta


@app.route('/api/v1/userRoute/signupUser', methods=['POST'])
def RegisterUser():
    conn = None
    cursor = None
    try:
        _json = request.json

        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']

        if _id and _name and _email and _password and request.method == 'POST':

            _hashed_password = generate_password_hash(_password)

            sql = "INSERT INTO user(user_id, user_name, user_email, user_password) VALUES(%s, %s, %s, %s)"
            data = (_id, _name, _email, _hashed_password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify(
                status='User added successfully!',
                name=_name

            )
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT user_id id, user_name name, user_email email, user_password pwd FROM user")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




@app.route('/api/v1/userRoute/signInUser')
def signInUser():
	id = request.headers['id']
	password = request.headers['password']
	conn = None
	cursor = None
	try:
		sql = "SELECT * FROM user WHERE user_id=%s"
		data = (id)
		conn = mysql.connect()
		cursor = conn.cursor()
		print('1')
		userID = cursor.execute(sql,data)
		print('2')
		row = cursor.fetchone()
		print('3')
		if userID :
			checkPassword = check_password_hash(row[3],password)
		print('4')
		# token = jwt.encode({
        # 	'public_id': id,
        # 	'exp': datetime.utcnow() + timedelta(minutes=30)
    	# 	}, app.config['SECRET_KEY'])

		# print('Token :',token)

		n = random.randint(10000000000,1000000000000000)

		if userID and checkPassword:
			resp = jsonify(
				StatusCode = 200,
				Token = n,
				user_id = row[0],
				user_name = row[1],
				user_email = row[2],
				massage = 'User ogged in successfully'
			)
		else:
			resp = jsonify(
				StatusCode = 403,
				massage = 'User NIC or password is incorrect'
			)
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/update', methods=['PUT'])
def update_user():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']

        if _name and _email and _password and _id and request.method == 'PUT':

            _hashed_password = generate_password_hash(_password)

            sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
            data = (_name, _email, _hashed_password, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/api/v1/orderRoute/placeOrder' , methods=['POST'])
def OrderItem():
	print("ok")
	conn = None
	Cursor = None
	print("ok2")
	try:
		print("ok3")
		_json = request.json
		print("ok4")
		_id = _json['id']
		_detail = _json['detail']
		_address = _json['address']
		_city = _json['city']
		print("ok5")
		_no = _json['no']
		_paymenttype = _json['paymenttype']
		_type = _json['type']
		_status = _json['status']
		_date = _json['date']
		_time = _json['time']
		print("ok6")
		print(_id,_detail,_address,_city,_no,_paymenttype,_type,_status)

		if _id and _detail and _address and _city and _no and _paymenttype and _type and _status and request.method == 'POST':
			print("ok7")
			sql = "INSERT INTO orderDetails(user_id,order_detail,order_delivery_address,order_city,contact_no,order_payment_type,order_type,order_status,order_date,order_time) VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
			data = (_id,_detail,_address,_city,_no,_paymenttype,_type,_status,_date,_time)
			print("ok8")
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql,data)
			print("ok9")
			conn.commit()
			resp = jsonify(
				status = 'User added successfully!',
			)
			resp.status_code = 200
			return resp
		
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/api/v1/orderRoute/orderStatus')
def getStatus():
	id = request.headers['id']
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM orderDetails WHERE user_id=%s", id)
		row = cursor.fetchall()
		resp = jsonify(row)
		print("----------------------")
		print(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp



if __name__ == "__main__":
    app.run(debug=true)

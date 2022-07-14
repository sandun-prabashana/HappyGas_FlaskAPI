
from fileinput import close
from colorama import Cursor
import pymysql
import pickle
from sqlalchemy import true
import numpy as np
from app import application
from db import mysql
from flask import request, jsonify
from flask import Flask
import jwt
import random
from flask import flash, request
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin

application = Flask(__name__)
cors = CORS(application, resources={r"/api/v1/adminRoute/*": {"origins": "*"}})

with open('Colombo.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Colombo =int(new_data[0, 0])

with open('DEHIWALA.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Dehiwala =int(new_data[0, 0])

with open('GALLE.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Galle =int(new_data[0, 0])

with open('GAMPAHA.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Gampaha =int(new_data[0, 0])

with open('KANDY.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Kandy =int(new_data[0, 0])

with open('KOLONNAWA.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Kolonnawa =int(new_data[0, 0])

with open('MAHARAGAMA.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Maharagama =int(new_data[0, 0])

with open('MORATUWA.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Moratuwa =int(new_data[0, 0])

with open('NEGAMBO.pkl', 'rb') as pickle_file:
	new_data = pickle.load(pickle_file)
	Negambo =int(new_data[0, 0])

Count = Colombo+Dehiwala+Maharagama+Moratuwa+Negambo+Galle+Gampaha+Kandy+Kolonnawa

@application.route('/test')
def hello():

	print (Count)
	return 'Welcome to happygas'


@application.route('/api/v1/userRoute/signupUser', methods=['POST'])
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


@application.route('/users')
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




@application.route('/api/v1/userRoute/signInUser')
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

@application.route('/update', methods=['PUT'])
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


@application.route('/delete/<id>', methods=['DELETE'])
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


@application.route('/api/v1/orderRoute/placeOrder' , methods=['POST'])
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

@application.route('/api/v1/orderRoute/orderStatus')
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

# ///////////////////////////////////////////////////////////////////////////////////////////////////////


@application.route('/api/v1/adminRoute/signInUser')
@cross_origin()
def signInAdminUser():
	email = request.headers['email']
	password = request.headers['password']
	conn = None
	cursor = None
	try:
		sql = "SELECT * FROM adminusers WHERE user_email=%s and user_password=%s"
		data = (email,password)
		conn = mysql.connect()
		cursor = conn.cursor()
		userID = cursor.execute(sql,data)
		row = cursor.fetchone()

		n = random.randint(10000000000,1000000000000000)

		if userID :
			resp = jsonify(
				StatusCode = 200,
				Token = n,
				user_nic = row[0],
				user_name = row[3],
				user_type = row[6],
                area = row[4],

				massage = 'User logged in successfully'
			)
		else:
			resp = jsonify(
				StatusCode = 403,
				massage = 'User Email or Password is incorrect'
			)
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@application.route('/api/v1/adminRoute/getAllUsers')
@cross_origin()
def getAllUsers():
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

@application.route('/api/v1/adminRoute/getAllSellers')
@cross_origin()
def getAllSellers():
	conn = None
	cursor = None
	type = "Seller"
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "select user_nic nic,user_email email,user_password password,user_name name,area area,user_no no from adminusers where user_type=%s"
		data = type
		cursor.execute(sql,data)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code =200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()



@application.route('/api/v1/adminRoute/deleteSellers', methods=['DELETE'])
@cross_origin()
def deleteSeller():
	nic = request.headers['nic']
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM adminusers WHERE user_nic=%s", (nic,))
		conn.commit()
		resp = jsonify(
				StatusCode = 200,
				massage = 'Seller Deleted Successful'
			)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@application.route('/api/v1/adminRoute/addSellers', methods=['POST'])
@cross_origin()
def addSeller():
	conn = None
	cursor = None
	try:
		_json = request.json

		_nic = _json['nic']
		_name = _json['name']
		_email = _json['email']
		_area = _json['area']
		_contact = _json['contact']
		_password = _json['password']
		_type = "SELLER"
		_qty = 0
		_date = _json['date']
		if _nic and _name and _email and _area and _contact and _password and request.method == 'POST':
			sql = "INSERT INTO adminusers(user_nic,user_email,user_password,user_name,area,user_no,user_type) VALUES (%s, %s, %s, %s ,%s, %s, %s)"
			data = (_nic, _email, _password, _name, _area, _contact, _type)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)

			if _area == 'Colombo':
				_qty=Colombo/12

			elif _area == 'Dehiwala':
				_qty = Dehiwala/12

			elif _area == 'Maharagama':
				_qty = Maharagama/12

			elif _area == 'Moratuwa':
				_qty = Moratuwa/12

			elif _area == 'Negambo':
				_qty = Negambo/12

			elif _area == 'Galle':
				_qty = Galle/12

			elif _area == 'Gampaha':
				_qty = Gampaha/12

			elif _area == 'Kandy':
				_qty = Kandy/12

			elif _area == 'Kolonnawa':
				_qty = Kolonnawa/12

			sql2 = "INSERT INTO distribut_gas(user_nic,qty,addedd_date) VALUES (%s, %s, %s)"
			data2 = (_nic, _qty, _date)
			cursor.execute(sql2, data2)

			sql3 = "INSERT INTO distribute_details(seller_nic, dispensing_amount, distribute_date) VALUES( %s, %s, %s)"
			data3 = (_nic, _qty, _date)
			cursor.execute(sql3, data3)

			conn.commit()

			resp = jsonify(
				status='Seller Added successfully!',
				statusCode=200
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




@application.route('/api/v1/adminRoute/getAllproduct')
@cross_origin()
def getAllProduct():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "select * from product"
		cursor.execute(sql)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code =200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@application.route('/api/v1/adminRoute/getAllproductStatus')
@cross_origin()
def getAllproductStatus():
	conn = None
	cursor = None
	status1 = "Completed"
	status2 = "Pending"
	status3 = "Delivering"
	status4 = "PickUp"
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "select count(order_id) orderCount from orderdetails"
		cursor.execute(sql)
		row = cursor.fetchone()

		sql2 = "select count(order_id) completeOrder from orderdetails where order_status=%s"
		data = status1
		cursor.execute(sql2,data)
		row2 = cursor.fetchone()

		sql3 = "select count(order_id) pendingOrder from orderdetails where order_status=%s"
		data2 = status2
		cursor.execute(sql3, data2)
		row3 = cursor.fetchone()

		sql4 = "select count(order_id) takeitOrder from orderdetails where order_status=%s"
		data3 = status4
		cursor.execute(sql4, data3)
		row4 = cursor.fetchone()

		sql5 = "select count(order_id) deliveryOrder from orderdetails where order_status=%s"
		data4 = status3
		cursor.execute(sql5, data4)
		row5 = cursor.fetchone()


		resp = jsonify(
			order = row,
			complete=row2,
			pending = row3,
			takeit = row4,
			delivery = row5
		)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@application.route('/api/v1/adminRoute/getQty', methods=['POST'])
@cross_origin()
def getQtyFromId():
    conn = None
    cursor = None
    nic = request.headers['nic']
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql2 = "select qty,a.user_name,a.area from distribut_gas d,adminusers a where a.user_nic=d.user_nic and d.user_nic=%s"
        data = nic
        qty = cursor.execute(sql2, data)
        row2 = cursor.fetchone()

        sql3 = "select qty from distribut_gas where distribut_id=%s"
        data3 = 1
        cursor.execute(sql3, data3)
        row3 = cursor.fetchone()

        if qty:
            resp = jsonify(
                StatusCode=200,
                data=row2,
                data2=row3
            )
            resp.status_code = 200
        else:
            resp = jsonify(
                StatusCode=403,
                massage='Seller Nic incorrect'
            )
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/api/v1/adminRoute/getAllQty')
@cross_origin()
def getAllQty():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select qty from distribut_gas where distribut_id=%s"
        data = 1
        cursor.execute(sql, data)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@application.route('/api/v1/adminRoute/updateQty', methods=['PUT'])
@cross_origin()
def updateQty():
    conn = None
    cursor = None
    try:
        _json = request.json
        _nic = _json['nic']
        _qty = _json['qty']
        _newAdminQty = _json['newAdminQty']
        _date = _json['date']

        if _nic and _qty and request.method == 'PUT':

            print(_nic)
            print(_qty)

            sql = "UPDATE distribut_gas SET qty=%s,addedd_date=%s WHERE user_nic=%s"
            data = (_qty,_date,_nic )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)


            sql2 = "UPDATE distribut_gas SET qty=%s,addedd_date=%s WHERE distribut_id=%s"
            data2 = (_newAdminQty,_date,1)
            cursor.execute(sql2, data2)
            conn.commit()
            resp = jsonify('Qty updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@application.route('/api/v1/adminRoute/addRecord', methods=['POST'])
@cross_origin()
def addSellrecord():
    conn = None
    cursor = None
    try:
        _json = request.json

        _nic = _json['nic']
        _qty = _json['qty']
        _date = _json['date']

        if _nic and _qty and _date and request.method == 'POST':

            sql = "INSERT INTO distribute_details(seller_nic, dispensing_amount, distribute_date) VALUES( %s, %s, %s)"
            data = (_nic, _qty, _date)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify(
                status='Distribut_details added successfully!',
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


@application.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@application.route('/api/v1/adminRoute/getAllRecord')
@cross_origin()
def getAllRecords():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "select * from distribute_details"
		cursor.execute(sql)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code =200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@application.route('/api/v1/adminRoute/getAllPickUpOrders', methods=['POST'])
@cross_origin()
def getAllPickUpOrders():
    conn = None
    cursor = None
    city = request.headers['city']
    try:
        print(city)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select o.order_id,u.user_name,o.order_detail,o.order_city,o.contact_no,o.order_payment_type,o.order_status,o.order_date from orderdetails o, user u where  o.order_type=%s and o.order_city=%s and u.user_id=o.user_id and o.order_status IN (%s,%s)"
        data =("PickUp",city,"Pending","PickUp")
        cursor.execute(sql,data)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@application.route('/api/v1/adminRoute/getAllDeliveryOrders', methods=['POST'])
@cross_origin()
def getAllDeliveryOrders():
    conn = None
    cursor = None
    city = request.headers['city']
    try:
        print(city)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select o.order_id,u.user_name,o.order_detail,o.order_city,o.order_delivery_address,o.contact_no,o.order_payment_type,o.order_status,o.order_date from orderdetails o, user u where  o.order_type=%s and o.order_city=%s and u.user_id=o.user_id and o.order_status IN (%s,%s)"
        data =("Delivery",city,"Pending","Delivering")
        cursor.execute(sql,data)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/api/v1/adminRoute/updateStatus', methods=['PUT'])
@cross_origin()
def updateOrderStatus():
	conn = None
	cursor = None
	try:
		_json = request.json
		_oid = _json['oid']
		_status = _json['status']

		print(type(_status))



		sql = "UPDATE orderdetails SET order_status=%s WHERE order_id=%s"
		data = (_status,_oid)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute(sql, data)
		conn.commit()
		resp = jsonify(
			status='Status Update successfully!',
		)
		resp.status_code = 200
		return resp

	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


@application.route('/api/v1/adminRoute/getAllOrderDetailForSeller', methods=['POST'])
@cross_origin()
def getAllOrderDetailForSeller():
	conn = None
	cursor = None
	_city = request.headers['city']
	_nic = request.headers['nic']
	try:

		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		sql = "select count(order_id) AllOrders from orderdetails  where order_city=%s"
		data = _city
		cursor.execute(sql,data)
		row = cursor.fetchone()

		sql2 = "select count(order_id) CompletedOrders from orderdetails where order_city=%s and order_status=%s"
		data2 = (_city,"Completed")
		cursor.execute(sql2,data2)
		row2 = cursor.fetchone()

		sql3 = "SELECT qty GasQty FROM  distribut_gas where user_nic=%s"
		data3 = _nic
		cursor.execute(sql3, data3)
		row3 = cursor.fetchone()



		resp = jsonify(
			order = row,
			complete=row2,
			gas = row3,
		)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@application.route('/api/v1/adminRoute/updateSellerQty', methods=['PUT'])
@cross_origin()
def updateSellerQty():
	conn = None
	cursor = None
	_qty = request.headers['qty']
	_nic = request.headers['nic']
	try:

		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "UPDATE distribut_gas SET qty=%s WHERE user_nic=%s"
		data = (_qty, _nic)
		cursor.execute(sql, data)
		conn.commit()
		resp = jsonify('Qty updated successfully!')
		resp.status_code = 200
		return resp

	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

if __name__ == "__main__":
    application.run(debug=true)

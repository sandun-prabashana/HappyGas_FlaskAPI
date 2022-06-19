import pymysql
from app import app
from db import mysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
		
@app.route('/add', methods=['POST'])
def add_user():
	conn = None
	cursor = None
	try:
		_json = request.json
        
        
		_id = _json['id']
        _name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		# validate the received values
		if _id and _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO user(user_id, user_name, user_email, user_password) VALUES(%s, %s, %s, %s)"
			data = (_id, _name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
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
    app.run()
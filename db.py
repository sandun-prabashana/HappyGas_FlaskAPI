from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
app.config['MYSQL_DATABASE_DB'] = 'happygas'
app.config['MYSQL_DATABASE_HOST'] = 'happygas.cye7dm9aermq.us-west-2.rds.amazonaws.com'

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
# app.config['MYSQL_DATABASE_DB'] = 'HappyGas'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
from app import application
from flaskext.mysql import MySQL

mysql = MySQL()

# application.config['MYSQL_DATABASE_USER'] = 'admin'
# application.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
# application.config['MYSQL_DATABASE_DB'] = 'happygas'
# application.config['MYSQL_DATABASE_HOST'] = 'happygas.cye7dm9aermq.us-west-2.rds.amazonaws.com'

application.config['MYSQL_DATABASE_USER'] = 'root'
application.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
application.config['MYSQL_DATABASE_DB'] = 'HappyGas'
application.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(application)
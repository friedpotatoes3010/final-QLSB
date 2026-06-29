import os

# If the project is configured to use MySQL via environment variables,
# allow PyMySQL to act as MySQLdb so Django can use the mysql backend.
if os.getenv('MYSQL_DATABASE'):
	try:
		import pymysql
		pymysql.install_as_MySQLdb()
	except Exception:
		# If PyMySQL not installed, Django will raise an informative ImportError later.
		pass

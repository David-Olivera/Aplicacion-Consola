import pyodbc
import MySQLdb
import ConfigParser
class conexion():
	global config
	#variables utilizadas para conectarse a Ms sql server
	global dsn;global uid;global pwd
	#variables utilizadas para la conexion con mysql
	global hostt; global userr; global passw; global bd
	"""def conectar_sql(self):
		config=ConfigParser.ConfigParser()
		config.read("Config/Configuracion.ini")
		#asignacion de valores para ms sql server 
		dsn=config.get("ConexionesMSSQLServer","dsn")
		uid=config.get("ConexionesMSSQLServer","uid")
		pwd=config.get("ConexionesMSSQLServer","pwd")

		ini_conex_sql="DSN="+dsn+";UID="+uid+";PWD="+pwd
		try:
			conectarms=pyodbc.connect(ini_conex_sql)
			cursorms=conectarms.cursor()
		except pyodbc.Error,err:
			print("No se puede conectar a la base de datos de MSSQLServer revisa los parametros...")
			#print(err)
		return cursorms, conectarms"""
	def conectar_mysql(self):
		config=ConfigParser.ConfigParser()
		config.read("Config/Configuracion.ini")
		#asignacion de valores para mysql
		hostt=config.get("ConexionesMySQL","host")
		userr=config.get("ConexionesMySQL","user")
		passw=config.get("ConexionesMySQL","pswd")
		bd=config.get("ConexionesMySQL","bd")
		try:
			ini_conex_mysql=MySQLdb.connect(host=hostt,user=userr,passwd=passw,db=bd)
			cursormysql=ini_conex_mysql.cursor()
			return cursormysql, ini_conex_mysql
		except MySQLdb.Error , err:
			print("No se puede conectar a la base de datos de MySQL revisa los parametros...")
			#pirnt(err)
			return 0,0
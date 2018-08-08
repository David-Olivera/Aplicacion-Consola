import os.path
import ConfigParser
from Mssql import *
from Correo import *
import time
class main():

	global classM
	classM=mssql()
		#self.iniciar()
	def iniciar(self):
		respuesta=self.validar_doc()
		if respuesta==False:
			self.crear_doc()
		else:
			#self.iniciar()
			classM.consul_slow()
			classM.consulta_blo()
		#classM=correo()
		#classM.enviar_correo()
		
	def validar_doc(self):
		b=True
		ruta="Config/Configuracion.ini"
		if os.path.isfile(ruta):
			print("Existen")
		else:
			print("Archivo de configuracion de la conexion no existe...")
			b=False
		return b

	def crear_doc(self):
		#import configparser
		config = ConfigParser.ConfigParser()

		print("Creando archivo de conexion...")
		#seccion de conexion de mysql
		config.add_section("ConexionesMSSQLServer")
		config.set("ConexionesMSSQLServer","DSN","MyMSSQLServer")
		config.set("ConexionesMSSQLServer","UID","sa")
		config.set("ConexionesMSSQLServer","PWD","1234")
		#Seccion de conexion de mysql
		config.add_section("ConexionesMySQL")
		config.set("ConexionesMySQL","HOST","192.168.56.1")
		config.set("ConexionesMySQL","USER","prueba")
		config.set("ConexionesMySQL","PSWD","1234")
		config.set("ConexionesMySQL","BD","proyectocedis")
		#seccion de configuracion del correo.
		config.add_section("Correo")
		config.set("Correo","remitente","da_sa1998@hotmail.com")
		config.set("Correo","password","david1998")
		config.set("Correo","destinatario","dasa.19983@gmail.com")
		config.set("Correo","smtp","smtp-mail.outlook.com:")
		config.set("Correo","puerto","587")

		config.add_section("Tiempo")
		config.set("Tiempo","Segundos","10")

		file=open("Config/Configuracion.ini","w")

		config.write(file)
		file.close()

		print("creando archivo para enviar correos...")
		#configco=ConfigParser
#config2 = ConfigParser.ConfigParser()
config2= ConfigParser.ConfigParser()
g=main()
while True:
	g.iniciar()
	config2.read("Config/Configuracion.ini")
	print("Vuelta S")
	#time.sleep(10)
	time.sleep(int(config2.get("Tiempo","segundos")))
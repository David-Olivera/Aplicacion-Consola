import pyodbc
import sqlparse
from Conexion import *
from Mysql import *
from Correo import *
import datetime
from datetime import datetime,date,time
from sqlparse import lexer
from sqlparse import sql, tokens as T
from sqlparse.compat import StringIO, text_type
import ConfigParser
import hashlib
class mssql():
	global diccionario_Memoria;global lista; global diccionario_update
	diccionario_Memoria={}
	diccionario_update={}
	lista={}
	def __init__(self):
		global classM; global classCo; global cursorms
		#classC=conexion()
		
		#conexion,put=classC.conectar_sql()
	def consul_slow(self):
		#print(diccionario_Memoria)
		classM=mysql()
		config=ConfigParser.ConfigParser()
		config.read("Config/Configuracion.ini")
		#asignacion de valores para ms sql server 
		dsn=config.get("ConexionesMSSQLServer","dsn")
		uid=config.get("ConexionesMSSQLServer","uid")
		pwd=config.get("ConexionesMSSQLServer","pwd")
		try:

			ini_conex_sql="DSN="+dsn+";UID="+uid+";PWD="+pwd
			conectarms=pyodbc.connect(ini_conex_sql)
			cursorms=conectarms.cursor()

			#Query de prueba
			#query="SELECT * FROM query WHERE hname=%s"
			#Este es el query Verdadero
			#---->
			#query="EXEC master.dbo.sp_WhoIsActive @get_outer_command = 1;"
			#<----
			query="EXEC master.dbo.sp_WhoIsActive @show_own_spid = 1, @get_outer_command = 1, @get_transaction_info = 1;"
			#conexion.execute(query)
			if len(diccionario_Memoria)==0:
				#cursorms.execute("SELECT * FROM query WHERE hname='salas';")
				cursorms.execute(query)
				for resultado in cursorms.fetchall():
					"""cpu=resultado[6]#<---here
					hname=resultado[17]#<---here
					dbn=resultado[18]#<---here
					st=resultado[14]#<---here
					usm=resultado[13]#<---here
					fech=datetime.now().strftime('%Y-%m-%d %I:%M:%S')#<---here
					sqlc=resultado[3]#<---here
					wait=resultado[0]#<---here"""
				
					
					"""cpu=int(resultado[1])
					hname=str(resultado[2])
					dbn=str(resultado[3])
					st=str(resultado[4])
					usm=int(resultado[5])
					fech=datetime.now().strftime('%Y-%m-%d %I:%M:%S')
					sqlc=str(resultado[6])
					wait=str(resultado[7])"""

					cpu=int(resultado[6])
					hname=str(resultado[17])
					dbn=str(resultado[18])
					st=str(resultado[14])
					usm=int(resultado[13])
					fech=datetime.now().strftime('%Y-%m-%d %I:%M:%S')
					sqlc=str(resultado[3])
					wait=str(resultado[0])

					sql_parser=self.parser_command(sqlc)
					sqlnp=sqlc
					sql_etiquetas=self.parser_etiquetas(sqlnp)
					sqlnp=sql_etiquetas
					sqlc=sql_parser
					#aqui comienza la comparacion en el diccionario
					datohash=self.md5_hash(sqlc)
					segundos=self.conver_segundos(wait)
					diccionario_Memoria[datohash]={"cpu": cpu, "hname": hname, "dbn": dbn,"st": st,"usm":usm,"fech":fech,"sqlc":sqlc,"wait":segundos,"sqlnp":sqlnp,"status":"Agregado"}
				#print(diccionario_Memoria)
			else:
				for llave in diccionario_Memoria.keys():
					valor=diccionario_Memoria[llave]
					valor['status']='Terminado'
				cursorms.execute("SELECT * FROM query WHERE hname='salas';")
				#cursorms.execute(query)
				for datoq in cursorms.fetchall():
					"""cpu=datoq[6]
					hname=datoq[17]
					dbn=datoq[18]
					st=datoq[14]
					usm=datoq[13]
					fech=datetime.now().strftime('%Y-%m-%d %I:%M:%S')
					sqlc=datoq[3]
					wait=datoq[0]"""
					"""cpu=datoq[1]
					hname=datoq[2]
					dbn=datoq[3]
					st=datoq[4]
					usm=datoq[5]
					fech=datetime.now().strftime('%Y-%m-%d %I:%M:%S')
					sqlc=datoq[6]
					wait=datoq[7]"""

					cpu=int(datoq[6])
					hname=str(datoq[17])
					dbn=str(datoq[18])
					st=str(datoq[14])
					usm=int(datoq[13])
					fech=datetime.now().strftime('%Y-%m-%d %I:%M:%S')
					sqlc=str(datoq[3])
					wait=str(datoq[0])

					sql_parser=self.parser_command(sqlc)
					sqlnp=sqlc
					sql_etiquetas=self.parser_etiquetas(sqlnp)
					sqlnp=sql_etiquetas
					sqlc=sql_parser
					datohash=self.md5_hash(sqlc)
					datoregresa=diccionario_Memoria.get(datohash)
					segundos=self.conver_segundos(wait)
					if datoregresa==None:
						diccionario_update[datohash]={"cpu": cpu, "hname": hname, "dbn": dbn,"st": st,"usm":usm,"fech":fech,"sqlc":sqlc,"wait":segundos,"sqlnp":sqlnp,"status":"Agregado"}
					else:
						for llaves in diccionario_Memoria.keys():
							if llaves==datohash:
								llavedato=diccionario_Memoria[llaves]
								llavedato['cpu']=cpu
								llavedato['hname']=hname
								llavedato['dbn']=dbn
								llavedato['st']=st
								llavedato['usm']=usm
								llavedato['fech']=fech
								llavedato['sqlc']=sqlc
								llavedato['wait']=segundos
								llavedato['sqlnp']=sqlnp
								llavedato['status']='Actualizado'
				diccionario_Memoria.update(diccionario_update)
				#print(diccionario_Memoria)

				lista=[]
				for envio in diccionario_Memoria.keys():
					datoenvio=diccionario_Memoria[envio]
					if datoenvio['status']== 'Terminado':
						lista.append(envio)
					else:
						pass
				if len(lista)>0:
					for lis in range(len(lista)):
						#empieza
						asignacion=lista[lis]
						print("Se encontro uno")
						classM.validacion_mysql(diccionario_Memoria[asignacion])
						#termina
						#print(lista[lis])
						diccionario_Memoria.pop(lista[lis])
					else:
						pass
					#aqui comienza el envio a la bd

		except pyodbc.InterfaceError:
			print("Rvisa los parametros del DSN")

		


	def parser_command(self,sql_command):
		sql=sql_command
		quitarG=sql.replace("--","")
		quitarE=quitarG.replace("?>","")
		quitarEP=quitarE.replace("<?query","")
		stream=lexer.tokenize(quitarEP)
		tokens=list(stream)
		Conta_Posi=0
		juntar=''
		for etiqueta in tokens:
			if tokens[Conta_Posi][0]==T.Number.Integer:
				juntar+='Int'
				Conta_Posi+=1
			elif tokens[Conta_Posi][0]==T.String.Symbol:
				juntar+='Str'
				Conta_Posi+=1
			elif tokens[Conta_Posi][0]==T.String.Single:
				juntar+='Str Sim'
				Conta_Posi+=1
			elif tokens[Conta_Posi][0]==T.String.Float:
				juntar+='Float'
				Conta_Posi+=1
			else:
				juntar+=etiqueta[1]
				Conta_Posi+=1
		return juntar

	def parser_etiquetas(self,sql_command):
		sql=sql_command
		quitarG=sql.replace("--","")
		quitarE=quitarG.replace("?>","")
		quitarEP=quitarE.replace("<?query","")
		return quitarEP

	def consulta_blo(self):
		classCo=correo()
		config=ConfigParser.ConfigParser()
		config.read("Config/Configuracion.ini")
		#asignacion de valores para ms sql server 
		dsn=config.get("ConexionesMSSQLServer","dsn")
		uid=config.get("ConexionesMSSQLServer","uid")
		pwd=config.get("ConexionesMSSQLServer","pwd")
		try:
			ini_conex_sql="DSN="+dsn+";UID="+uid+";PWD="+pwd
			conectarms=pyodbc.connect(ini_conex_sql)
			cursorms=conectarms.cursor()
		except pyodbc.InterfaceError:
			print("Revisa los parametros de DSN")

		query="EXEC master.dbo.sp_WhoIsActive @find_block_leaders=1;"
		try:
			cursorms.execute(query)
			#cursorms.execute("SELECT * FROM query WHERE hname='salas';")
			for resultado in cursorms.fetchall():
				ids=resultado[1]
				sql_c=resultado[2]
				db=resultado[18]
				dix={"ids":ids,"sql_c":sql_c,"db":db}
				print(dix["db"])
				print("Se encontro un bloqueo")
				classCo.enviar_correo(dix)
		except UnboundLocalError:
			print("Revisa los parametros del DSN")

	def validar_existencia(self,valor):
		for datos in diccionario_Memoria.keys():
			if datos == valor :
				diccionario_Memoria[valor]={}
			else:
				diccionario_Memoria[valor]={}

	def md5_hash(self,query):
		cadena=query.encode('utf-8')
		hashMD5=hashlib.md5(cadena).hexdigest()
		return hashMD5


	def conver_segundos(self,tiempo):
		dias,tiempo=tiempo.split()
		DiasSeg=float((int(dias)*24)*3600)
		horas,minutos,segundos=tiempo.split(":")
		horas_segundos=int(horas)*3600
		minutos_segundos=int(minutos)*60
		segundos_conver=float(segundos)
		suma=float(DiasSeg+horas_segundos+minutos_segundos+segundos_conver)
		return suma






import hashlib
from Conexion import *
import MySQLdb
from MySQLdb import *
import ConfigParser
class mysql():

	global classC;global conexion;global put
	classC=conexion()
	conexion,put=classC.conectar_mysql()
	def __init__(self):
		pass
	def validacion_mysql(self,dic):
		#print(type(dic['sqlc']))
		resultado=self.md5_sql(str(dic['sqlc']))
		existe=self.existe_sql(resultado)
		if existe== False:
			self.insertar_query(dic,resultado)
			self.insertar_ocu(resultado,dic['fech'],dic['sqlnp'],dic['wait'],dic['cpu'],dic['usm'])
		else:
			self.update_query(resultado,dic['fech'],dic['wait'],dic['usm'],dic['cpu'])
			#self.seleccionar_ocu(resultado,dic['fech'])
			self.insertar_ocu(resultado,dic['fech'],dic['sqlnp'],dic['wait'],dic['cpu'],dic['usm'])

	def insertar_query(self,valores,id):
		cpu=valores['cpu']
		#cpuE=cpu.replace(" ","")
		hname=valores['hname']
		dbn=valores['dbn']
		st=valores['st']
		usm=valores['usm']
		fech=valores['fech']
		sqlc=valores['sqlc']
		wait=valores['wait']
		#print(float(cpuE))
		#print(type(cpuE))
		try:
			conexion.execute("INSERT INTO query(IdQuery,cpu,hostname,databasename,status,usedmemory,sqlcommand,wait,FechaQ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,cpu,valores["hname"],valores["dbn"],valores["st"],valores["usm"],valores["sqlc"],valores["wait"],valores["fech"]))
			put.commit()
			print("Se inserto")
		except MySQLdb.MySQLError as e:
			print("Error en el query"+e)

	def update_query(self,id,fecha,wait,memory,cpu):
		#cpuE=cpu.replace(" ","")
		#print(float(cpuE))
		#print(type(cpuE))
		print(type(memory))
		conexion.execute("UPDATE query SET FechaQ=%s, cpu=%s, usedmemory=%s, wait=%s WHERE IdQuery=%s",(fecha,cpu,memory,wait,id))
		put.commit()
		print("Se actualizo")

	def existe_sql(self,sql_command):
		conta=0
		existe=False
		conexion.execute("SELECT IdQuery FROM query WHERE IdQuery='"+sql_command+"'")
		for contador in conexion.fetchall():
			conta+=1
		if conta>0:
			existe=True
		print("existe query")
		return existe

	def md5_sql(self,hash_q):
		cadena=hash_q.encode('utf-8')
		hashMD5=hashlib.md5(cadena).hexdigest()
		return hashMD5
	def insertar_ocu(self,id,fecha,sql,wait,cpu,usm):
		#cpuE=cpu.replace(" ","")
		#print(float(cpuE))
		#print(type(cpuE))
		conexion.execute("INSERT INTO ocurrencia(IdQuery,sqlcommand,wait,cpu,usedmemory,FechaO) VALUES(%s,%s,%s,%s,%s,%s)",(id,sql,wait,cpu,usm,fecha))
		put.commit()
		print("inserta ocurrencia")

	"""def seleccionar_ocu(self,id,fecc):
		#idO='';canO='';fec=''
		conexion.execute("SELECT IdOcurrencia,CantidadO,FechaO FROM ocurrencia WHERE IdQuery=%s AND FechaO=%s",(id,fecc))
		if len(conexion.fetchall())==0:
			#aqui insertaria esa madre wey
			print("vacio")
			self.insertar_ocu(id,fecc)
		else:
			conexion.execute("SELECT IdOcurrencia,CantidadO,FechaO FROM ocurrencia WHERE IdQuery=%s AND FechaO=%s",(id,fecc))
			for resultado in conexion.fetchall():
				#print(resultado)
				idO=resultado[0]
				canO=resultado[1]
				fec=resultado[2]
			#aqui regresaria los valores
			self.update_ocu(idO,canO,fec)
			#return idO,canO,fec
			#print(canO)
			#print(idO)


	def update_ocu(self,id,cantidad,fecha):
		cantidadSuma=''
		print(cantidad)
		cantidadSuma=cantidad+1
		conexion.execute("UPDATE ocurrencia SET CantidadO=%s WHERE IdOcurrencia=%s AND FechaO=%s",(cantidadSuma,id,fecha))
		put.commit()
		if put.commit()==True:
			print("yes")
		else:
		self.insertar_ocu(idquery,fecha)"""

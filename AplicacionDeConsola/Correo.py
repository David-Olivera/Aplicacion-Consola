import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ConfigParser

class correo():

	def enviar_correo(self,dic):
		config=ConfigParser.ConfigParser()
		ruta="Config/Configuracion.ini"
		config.read(ruta)
		remitente=config.get("Correo","remitente")
		password=config.get("Correo","password")
		destinatario=config.get("Correo","destinatario")
		Subject="Bloqueo Encontrado"
		msg=MIMEMultipart()
		msg['From']=remitente
		msg['To']=destinatario
		msg['Subject']=Subject
		#en este apartado es donde se agrega el correo y se pone que es de texto plano
		print(dic["db"])
		mensaje=MIMEText("Se encontro un bloqueo en la BD "+dic["db"]+" con el id de sesion "+str(dic["ids"])+" y la consulta  "+dic["sql_c"],'plain')
		#se agrega el mensaje al correo
		msg.attach(mensaje)
		try:
			#Se crea el objeto smtp para outlook
			server = smtplib.SMTP(config.get("Correo","smtp")+config.get("Correo","puerto"))
			server.ehlo()
			#se inicia el objeto
			server.starttls()
			#Se debe e loguear el usuario que quiere enviar el correo
			server.login(remitente,password)
			#se envia el correo y el mensaje se debe convertir a un stream
			server.sendmail(remitente,destinatario,msg.as_string())
			print("Se envio")
			server.quit()
		except:
			print("No se pueden enviar correos revisa el SMTP")
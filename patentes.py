from bs4 import BeautifulSoup
import requests
import json
from imagesoup import ImageSoup
from flask import render_template
import webbrowser
import basic_example

def datos_persona(rut):

	url = "https://api.rutify.cl/rut/%s" % rut
	peticion = requests.get(url)
	datosruti = json.loads(peticion.content)
	datos_persona.nombre = datosruti["nombre"].upper()
	datos_persona.rut = datosruti["rut"]
	if datosruti["sexo"] == 1:
		datos_persona.sexo = "Masculino"
	else:
		datos_persona.sexo = "Femenino"
	datos_persona.comuna = datosruti["servel"]["comuna"]
	datos_persona.domicilio = datosruti["servel"]["domicilio electoral"]
	datos_persona.pais = datosruti["servel"]["pais"]

# CHECKBOX INDEX DIRECCION EN GOOGLE
	if basic_example.request.form.get('googlemap'):
		print("CHECKBOX - Mostrando mapa")

		direccionlala = datos_persona.domicilio
		print(direccionlala)
		direccionlala = direccionlala.split()
		print(direccionlala)

		if len(direccionlala)>2:
			print (" ".join(direccionlala[:3]))
			direccionlala = (" ".join(direccionlala[:3]))
			print("3"+direccionlala)
			print('https://www.google.com/maps/place/' + str(direccionlala) + " " + str(datos_persona.comuna))

			try:
				webbrowser.open('https://www.google.com/maps/place/' + str(direccionlala) + " " + str(datos_persona.comuna))
			except:
				print("Error mostrando mapa if")

		else:
			print('https://www.google.com/maps/place/' + datos_persona.domicilio + " " + datos_persona.comuna)

			try:
				webbrowser.open('https://www.google.com/maps/place/' + datos_persona.domicilio + " " + datos_persona.comuna)
			except:
				print("Error mostrando mapa else")

	else:
		print("NO CHECKBOX - No mostrando mapa")


def multas(patente):

	campos = ["Patente","Rut","Nombre","Monto","Año","Motivo","Comuna",]
	datacampos = []

	url = "https://www.sem.gob.cl/pcirc/buscar_multas.php?&tipo=0&patente=%s&rut=0" % patente
	peticion = requests.get(url)
	peticiontxt = peticion.text

	soup = BeautifulSoup(peticiontxt,'html.parser')
	multas.multass=0

	try:
		contador=0
		for data in soup.find_all('th'):
			# print(data)
			data = str(data)
			if contador >= 7:
				datacampos.append(data[4:-5])
				# print(contador,data[4:-5])
			else:
				pass
			contador+=1
			# print(datacampos)
		dictionary=dict(zip(campos,datacampos))
		print(dictionary)
		if len(dictionary) < 4:
			print("No multas")
			multas.multass=1
		else:
			print("OK")
			# multas.patente=dictionary["Patente"]
			multas.rut=dictionary["Rut"]
			multas.nombre=dictionary["Nombre"]
			multas.monto=dictionary["Monto"]
			multas.ano=dictionary["Año"]
			multas.motivo=dictionary["Motivo"]
			multas.comuna=dictionary["Comuna"]

	except:
		print("No multas o error buscando patente")

def tipoVehiculo(numero):

	if numero == "1":
		tipo = 'AUTOMOVIL'
	elif numero == "2":
		tipo = 'STATION WAGON'
	elif numero == "3":
		tipo = 'TODO TERRENO'
	elif numero == "4":
		tipo = 'CAMIONETA'
	elif numero == "5":
		tipo = 'FURGON'
	elif numero == "7":
		tipo = 'CARRO DE ARRASTRE'
	elif numero == "12":
		tipo = 'MOTOCICLETA'
	else:
		tipo = 'Otro'

	return tipo

def datos_persona_auto(patente):

	try:
		url = "https://soap.uanbai.com/bci/soap/2018/ajax/loadPPU.jsp?PPU=%s&SES=DDB9674E703F9BB04C4F3BB2D96D8291.worker1" % patente
		peticion = requests.get(url)
		datos = json.loads(peticion.content)

	except:
		print ("\nNo se pudo obtener la información (SOAP)")

	# try:
	# Datos del dueño

	datos_persona_auto.nombredueno = (datos['propietario']['nombre'] + " " + datos['propietario']['ap_paterno'] + " " + datos['propietario']['ap_materno'])
	datos_persona_auto.rut = (datos['propietario']['rut'] +"-" + datos['propietario']['dv'])
	
	print(datos_persona_auto.rut)

	# OBTENER DATOS DE DOMICIO ELECTORAL RUTIFY

	try:
		url = "https://api.rutify.cl/rut/%s" % datos_persona_auto.rut
		peticion = requests.get(url)
		datosruti = json.loads(peticion.content)
		datos_persona_auto.datosrutii = str(datosruti)

		

		# print(datos_persona_auto.datosrutii)

		datos_persona_auto.nombre = datosruti["nombre"]
		datos_persona_auto.rut = datosruti["rut"]
		if datosruti["sexo"] == 1:
			datos_persona_auto.sexo = "Masculino"
		else:
			datos_persona_auto.sexo = "Femenino"
		datos_persona_auto.comuna = datosruti["servel"]["comuna"]
		datos_persona_auto.domicilio = datosruti["servel"]["domicilio electoral"]
		datos_persona_auto.pais = datosruti["servel"]["pais"]


# CHECKBOX INDEX DIRECCION EN GOOGLE

		if basic_example.request.form.get('googlemap'):
			print("CHECKBOX - Mostrando mapa")

			direccionlala = datos_persona_auto.domicilio
			print(direccionlala)
			direccionlala = direccionlala.split()
			print(direccionlala)

			if len(direccionlala)>2:
				print (" ".join(direccionlala[:3]))
				direccionlala = (" ".join(direccionlala[:3]))
				print("3"+direccionlala)
				print('https://www.google.com/maps/place/' + str(direccionlala) + " " + str(datos_persona_auto.comuna))

				try:
					webbrowser.open('https://www.google.com/maps/place/' + str(direccionlala) + " " + str(datos_persona_auto.comuna))
				except:
					print("Error mostrando mapa if")

			else:
				print('https://www.google.com/maps/place/' + datos_persona_auto.domicilio + " " + datos_persona_auto.comuna)

				try:
					webbrowser.open('https://www.google.com/maps/place/' + datos_persona_auto.domicilio + " " + datos_persona_auto.comuna)
				except:
					print("Error mostrando mapa else")

		else:
			print("NO CHECKBOX - No mostrando mapa")


	except:
		datos_persona_auto.errorruti=datosruti["error"]
		print("Error sacando info de rutify")


	# Datos del vehiculo
	try:

		datos_persona_auto.tipovehi = (tipoVehiculo(datos['id_tipo']))
		
		print(datos_persona_auto.tipovehi)

		datos_persona_auto.marcavehi = (datos['marca'])
		datos_persona_auto.modelovehi = (datos['modelo'])
		datos_persona_auto.anoauto = (str(datos['ano']))
		datos_persona_auto.nmotor = (str(datos['vin']))
		datos_persona_auto.dvpatente = (str(datos['dvpatente']))


		# Busqueda de imagenes en google del modelo del auto
		# Problema con mostrar imagenes de webs sin https

		busqueda = (datos_persona_auto.marcavehi,datos_persona_auto.modelovehi,datos_persona_auto.anoauto)

		auto = ImageSoup()

		images = auto.search(busqueda, n_images=4)

		datos_persona_auto.firstimage = images[0].URL
		datos_persona_auto.secondimage = images[1].URL
		datos_persona_auto.thirdimage = images[2].URL

	except:
		print("datos auto error")

	# except:
	# 	print("Error dato info de Persona")
from bs4 import BeautifulSoup
import requests
import json
from imagesoup import ImageSoup
from flask import render_template
# import webbrowser

def datos_persona(rut):

	url = "https://api.rutify.cl/rut/%s" % rut
	peticion = requests.get(url)
	datosruti    = json.loads(peticion.content)
	datos_persona.nombre = datosruti["nombre"].upper()
	datos_persona.rut = datosruti["rut"]
	if datosruti["sexo"] == 1:
		datos_persona.sexo = "Masculino"
	else:
		datos_persona.sexo = "Femenino"
	datos_persona.comuna = datosruti["servel"]["comuna"]
	datos_persona.domicilio = datosruti["servel"]["domicilio electoral"]
	datos_persona.pais = datosruti["servel"]["pais"]

	# webbrowser.open('https://www.google.com/maps/place/' + datos_persona.domicilio+" " +datos_persona.comuna)

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
		datos    = json.loads(peticion.content)

	except:
		print ("\nNo se pudo obtener la información (SOAP)")

	# Datos del dueño
	datos_persona_auto.nombredueno = (datos['propietario']['nombre'] + " " + datos['propietario']['ap_paterno'] + " " + datos['propietario']['ap_materno'])
	datos_persona_auto.rut = (datos['propietario']['rut'] +"-" + datos['propietario']['dv'])
	
	print(datos_persona_auto.rut)
	if datos_persona_auto.rut == '0-0':
		print("ERROR INFO SOAP")
	else:
		pass

	# OBTENER DATOS DE DOMICIO ELECTORAL RUTIFY
	url = "https://api.rutify.cl/rut/%s" % datos_persona_auto.rut
	peticion = requests.get(url)
	datosruti    = json.loads(peticion.content)
	datos_persona_auto.datosrutii = str(datosruti)
	# print(datosrutii)

	datos_persona_auto.nombre = datosruti["nombre"]
	datos_persona_auto.rut = datosruti["rut"]
	if datosruti["sexo"] == 1:
		datos_persona_auto.sexo = "Masculino"
	else:
		datos_persona_auto.sexo = "Femenino"
	datos_persona_auto.comuna = datosruti["servel"]["comuna"]
	datos_persona_auto.domicilio = datosruti["servel"]["domicilio electoral"]
	datos_persona_auto.pais = datosruti["servel"]["pais"]


	# Datos del vehiculo
	
	datos_persona_auto.tipovehi = (tipoVehiculo(datos['id_tipo']))
	datos_persona_auto.marcavehi = (datos['marca'])
	datos_persona_auto.modelovehi = (datos['modelo'])
	datos_persona_auto.anoauto = (str(datos['ano']))
	datos_persona_auto.nmotor = (str(datos['vin']))
	datos_persona_auto.dvpatente = (str(datos['dvpatente']))

	marca = datos_persona_auto.marcavehi
	modelo = datos_persona_auto.modelovehi
	ano = datos_persona_auto.anoauto

	busqueda = (marca,modelo,ano)

	auto = ImageSoup()
	images = auto.search(busqueda, n_images=5)

	firstimage = images[0]
	firstimage = str(firstimage)

	secondimage = images[1]
	secondimage = str(secondimage)

	thirdimage = images[2]
	thirdimage = str(thirdimage)

	datos_persona_auto.primeraimagen = firstimage[13:-2]
	datos_persona_auto.segundaimagen = secondimage[13:-2]
	datos_persona_auto.terceraimagen = thirdimage[13:-2]

	# print(datos_persona_auto.primeraimagen)

	# print(datos_persona_auto.primeraimagen,datos_persona_auto.segundaimagen,datos_persona_auto.terceraimagen)

def multas(patente):

	campos = ["Patente","Rut","Nombre","Monto","Año","Motivo","Comuna",]
	datacampos = []

	url = "https://www.sem.gob.cl/pcirc/buscar_multas.php?&tipo=0&patente=%s&rut=0" % patente
	peticion = requests.get(url)
	peticiontxt    = peticion.text

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
			multas.patente=dictionary["Patente"]
			multas.rut=dictionary["Rut"]
			multas.nombre=dictionary["Nombre"]
			multas.monto=dictionary["Monto"]
			multas.ano=dictionary["Año"]
			multas.motivo=dictionary["Motivo"]
			multas.comuna=dictionary["Comuna"]

	except:
		print("No multas o error buscando patente")



# multas("DSFS12")
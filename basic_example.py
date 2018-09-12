from flask import Flask, render_template, request
import requests
import json
import patentes

app = Flask(__name__)

def errores():
	@app.errorhandler(403)
	def errorhandler403(e):
		return render_template('403.html'), 403

	@app.errorhandler(404)
	def errorhandler404(e):
		return render_template('404.html'), 404

	@app.errorhandler(410)
	def errorhandler410(e):
		return render_template('410.html'), 410

	@app.errorhandler(500)
	def errorhandler500(e):
		return render_template('500.html'), 500

errores()

@app.route('/')
def index():
	return render_template('index.html')

checkboxgoogle=0

@app.route('/inforut', methods=['POST'])
def rutpersona():
	rut = request.form['rut_persona']

	patentes.datos_persona(rut)

	return render_template('inforut.html', 
							nombre=patentes.datos_persona.nombre,
							rut=patentes.datos_persona.rut,
							sexo=patentes.datos_persona.sexo,
							comuna=patentes.datos_persona.comuna,
							domicilio=patentes.datos_persona.domicilio,
							pais=patentes.datos_persona.pais)

@app.route('/infopatente', methods=['POST'])
def patenteauto():
	patente = request.form['patente_auto']

	patentes.datos_persona_auto(patente)

	if patentes.datos_persona_auto.rut == '0-0':
		print("asdasdasdasdasdasd 0-0 ")
		return render_template('errorsoap.html',error=patentes.datos_persona_auto.rut)

	if patentes.datos_persona_auto.datosrutii == "{'error': 'User not found'}":
		return render_template('rutnotfoundrutify.html',error=patentes.datos_persona_auto.errorruti)

	else:
		return render_template('infopatente.html',
							patente=patente.upper(),
							nombredueno=patentes.datos_persona_auto.nombredueno,
							rut=patentes.datos_persona_auto.rut,
							sexo=patentes.datos_persona_auto.sexo,
							domicilio=patentes.datos_persona_auto.domicilio,
							comuna=patentes.datos_persona_auto.comuna,
							pais=patentes.datos_persona_auto.pais,
							tipovehi=patentes.datos_persona_auto.tipovehi,
							marcavehi=patentes.datos_persona_auto.marcavehi,
							modelovehi=patentes.datos_persona_auto.modelovehi,
							anoauto=patentes.datos_persona_auto.anoauto,
							nmotor=patentes.datos_persona_auto.nmotor,
							dvpatente=patentes.datos_persona_auto.dvpatente,
							primeraimagen=patentes.datos_persona_auto.firstimage,
							segundaimagen=patentes.datos_persona_auto.secondimage,
							terceraimagen=patentes.datos_persona_auto.thirdimage)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 32783)

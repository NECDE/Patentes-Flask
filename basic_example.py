from flask import Flask, render_template, request
import requests,json,patentes

app = Flask(__name__)

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

@app.route('/')
def index():
	return render_template('index.html')

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
	# patentes.multas(patente)
	# if patentes.multas.multass==1:
	# 	patentes.multas.patente='Null'
	# 	patentes.multas.rut='Null'
	# 	patentes.multas.nombre='Null'
	# 	patentes.multas.monto='Null'
	# 	patentes.multas.ano='Null'
	# 	patentes.multas.motivo='Null'
	# 	patentes.multas.comuna='Null'
	# else:
	# 	pass
	try:
		patentes.datos_persona_auto(patente)
	except:
		print("404 try")
		return render_template('404.html')

	if patentes.datos_persona_auto.datosrutii == "{'error': 'User not found'}":
		print("\nUser not found\n")
		print("404 if")
		return render_template('404.html')
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
							# multa_patente=patentes.multas.patente,
							# multa_rut=patentes.multas.rut,
							# multa_nombre=patentes.multas.nombre,
							# multa_monto=patentes.multas.monto,
							# multa_ano=patentes.multas.ano,
							# multa_motivo=patentes.multas.motivo,
							# multa_comuna=patentes.multas.comuna,
							primeraimagen=patentes.datos_persona_auto.primeraimagen,
							segundaimagen=patentes.datos_persona_auto.segundaimagen,
							terceraimagen=patentes.datos_persona_auto.terceraimagen)

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80)

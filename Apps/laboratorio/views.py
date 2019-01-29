# -*- coding: utf-8 -*-
from __future__						import unicode_literals
# Importaciones de Django
from datetime						import datetime, timedelta
from django.conf 					import settings
from django.contrib.auth.decorators	import login_required
from django.core.mail				import EmailMultiAlternatives, EmailMessage
from django.db.models				import Count
from django.http					import HttpResponseRedirect, HttpResponse
from django.shortcuts				import render, get_list_or_404, get_object_or_404
from django.urls					import reverse, reverse_lazy
from django.views.generic			import ListView, DetailView, CreateView, DeleteView

# Para imprimir el PDF
from io								import BytesIO
from reportlab.lib 					import colors
from reportlab.lib.enums			import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes 		import A4, cm
from reportlab.lib.styles 			import getSampleStyleSheet
from reportlab.pdfgen 				import canvas
from reportlab.platypus 			import SimpleDocTemplate, Paragraph, TableStyle, Table

# Desde otra Apps
from Apps.catedras.models			import (
											Materia,
											)
from Apps.usuarios.models			import (
											Alumno,
											Docente,
											)
# Desde esta App
from Apps.laboratorio.forms			import (
											Fomulario_Crear_Horario,
											Formulario_Borrar_Horario,
											)
from Apps.laboratorio.models		import (
											Laboratorio,
											Comision,
											Inscripcion,
											Horario,
											WeekDay,
											)


# Funcion de Vista para enlistar las materias
def Listar_Laboratorio(request, slug):

	# Obtenemos la materia
	mat = Materia.objects.get(slug = slug)
	# Obtenemos los laboratorios de la materia
	lab = Laboratorio.objects.filter(materia = mat)
	# Creamos el contexto
	context =({
		'materia': mat,
		'laboratorios':lab,
		})

	# Renderizamos el contexto
	return render (request, 'laboratorio/lista.html', context)


# Funcion de Vista para Detallar el laboratorio y sus comisiones
def Detalle_del_Laboratorio(request, slug):
	# Obtenemos el laboratorio en funcion de la url
	lab = Laboratorio.objects.get(slug= slug)
	# Obtenemos la mateia del laboratorio
	mat = lab.materia
	# Obtenemos los horarios para esta materia
	hor = Horario.objects.filter(materia = mat)
	# obtenemos las comisiones de la materia
	comisiones = Comision.objects.filter(horario__in=hor)
	# Obtenemos todas las comisones en el rango del laboratorio
	coms = comisiones.filter(fecha__range=(lab.fecha_inicio, lab.fecha_fin))
	# Obtenemos los id de los horarios
	turn = coms.values_list('turno')
	# Obtenemos los horarios de las comisiones
	horarios = hor.filter(turno__in=turn)
	
	# Obtenemos la lista de horarios para los laboratorios, filtrados por dia de la semana
	lunes = horarios.filter(dia_semana=0)
	martes = horarios.filter(dia_semana=1)
	miercoles = horarios.filter(dia_semana=2)
	jueves = horarios.filter(dia_semana=3)
	viernes = horarios.filter(dia_semana=4)
	sabado = horarios.filter(dia_semana=5)
	domingo = horarios.filter(dia_semana=6)


	# Consultamos si el User pertenece al grupo "docente"
	if request.user.groups.filter(name='docente').exists():
		# Si es "laboratorista"
		# Redireccionamos al "Home"
		return HttpResponseRedirect(reverse('home'))

	# Consultamos si el User pertenece al grupo "laboratorista"
	if request.user.groups.filter(name='laboratorista').exists():
		# Si es "laboratorista"
		# Obtenemos las comisiones
		com = coms
		# Filtramos las comisiones del laboratorio por fecha y hora
		# Verificamos que el metodo sea GET y que exista la Variable "horario"
		if request.method == 'GET' and 'horario' in request.GET:
			# Si existe
			# Tomamos el valor de la variable
			horario = request.GET['horario']
			if horario == 'all': # horario = all
				# Mostramos todas las comisiones
				com = coms
			else:
				# horario = dhh (numero que identifica al dia de la semana y hora de inicio)
				# Mostramos las comisiones filtradas
				com = coms.filter(turno=horario)
		else:
			# Si no existe
			# Mostramos todas las comisiones
			com = coms

	# Consultamos si el User pertenece al grupo "alumno"
	if request.user.groups.filter(name='alumno').exists():
		# Si es "alumno"
		# Obtenemos la fecha de hoy
		hoy = datetime.now()
		# Excluimos las comisiones del laboratorio de fechas pasadas y con cupo lleno
		com = coms.exclude(fecha__range=(lab.fecha_inicio, hoy)).exclude(anotados= lab.cupo)
		# Filtramos las comisiones del laboratorio por fecha y hora
		# Verificamos que el metodo sea GET y que exista la Variable "horario"
		if request.method == 'GET' and 'horario' in request.GET:
			# Si existe
			# Tomamos el valor de la variable
			horario = request.GET['horario']
			if horario == 'all': # horario = all
				# Mostramos todas las comisiones
				com = coms
			else:
				# horario = dhh (numero que identifica al dia de la semana y hora de inicio)
				# Mostramos las comisiones filtradas
				com = coms.filter(turno=horario)
		else:
			# Si no existe
			# Mostramos todas las comisiones
			com = coms

	# Creamos el contexto

	context =({
		'laboratorio': lab,
		'comisiones': com,
		'lunes': lunes,
		'martes': martes,
		'miercoles': miercoles,
		'jueves': jueves,
		'viernes': viernes,
		'sabado': sabado,
		'domingo': domingo,
		})
	# Renderizamos el contexto
	return render (request, 'laboratorio/detalles.html', context)


# Funcion de Vista para Confirmar y Guardar la inscripcion del laboratorio
def Inscripcion_Laboratorio(request, laboratorio_id, comision_id):
	if request.user.groups.filter(name='alumno').exists():
		#Verificamos si el metodo es POST
		if request.method == 'POST':
			# SI es POST
			# Obtenemos el laboratorio y la comision, con los parametros de la url
			lab = Laboratorio.objects.get(id= laboratorio_id)
			com = Comision.objects.get(id= comision_id)
			# Obtenemos datos del laboratorio y la comision para mostrar en el template
			laboratorio_nombre = lab.nombre # Nombre del laboratorio
			fecha_com = com.fecha # Fecha para la que se inscribio
			horainicio = com.horario.hora_inicio # Hora en la que se inscribio
			# Creamos el contexto
			context = ({
				'laboratorio': laboratorio_nombre,
				'fecha': fecha_com,
				'hora': horainicio,
				})
			# Verificamos la confirmacion de la inscripcion
			if request.method =='POST' and 'opcion' in request.POST:
				opcion = request.POST['opcion']
				if opcion == 'si': # opcion=si
					# Confirma la inscripcion
					# Iniciamos una instancia, y asignamos los valores a los campos
					i = Inscripcion(
						alumno = Alumno.objects.get(user=request.user),
						comision = com,
						laboratorio = lab,
						)
					i.save() #guardamos la inscripcion en la DB
					# Sumamos 1 al numero de "anotados" de la comision
					com.anotados = com.anotados+1
					# Actualizamos la comision
					com.save()
					# Redireccionamos al Home
					return HttpResponseRedirect(reverse('home'))
				else: # opcion=no
					# Cancela la inscripcion
					# Redireccionamos al detalle del laboratorio
					return HttpResponseRedirect(reverse('detalle_laboratorio', args=[lab.slug]))
		else:
		# NO es POST
			# Redireccionamos al la lista de laboratorios
			return HttpResponseRedirect(reverse('laboratorios'))
	else:
	# NO es alumno
		# Redireccionamos al home
		return HttpResponseRedirect(reverse('home'))

	return render (request, 'inscripcion/crear_confirmar.html', context)


# Vita de los laboratorios en los que estoy inscripto
def Mis_Laboratorios(request):
	if request.user.groups.filter(name='alumno').exists():
		# Obtenemos al alumno
		alu = Alumno.objects.get(user=request.user)
		# Filtramos las inscripciones por ususario
		ins = Inscripcion.objects.filter(alumno=alu)
		# Generamos el contexto
		context =({
			'mis_laboratorios': ins,
			})
		# Renderizamos el contexto
		return render (request, 'laboratorio/mis_laboratorios.html', context)
	else:
	# NO es alumno
		# Redireccionamos al home
		return HttpResponseRedirect(reverse('home'))


# Vista para Confirmar y Borrar la inscripcio
def Cancelar_Inscripcion(request, inscripcion_id):
	if request.user.groups.filter(name='alumno').exists():
		# Verificamos si el metodo es POST
		if request.method == 'POST':
			# Si es POST
			# Obtenemos la inscripcion y la comision, con los parametros de la url
			ins = Inscripcion.objects.get(id = inscripcion_id)
			com = Comision.objects.get(id = ins.comision.id)
			# Obtenemos datos del laboratorio y la comision para mostrar en el template
			laboratorio_nombre = ins.laboratorio.nombre # Nombre del laboratorio
			fecha_com = ins.comision.fecha # Fecha para la que se inscribio
			# Creamos el contexto
			context = ({
				'laboratorio': laboratorio_nombre,
				'fecha': fecha_com,
				})
			# Verificamos la confirmacion de la cancelacion de la inscripcion
			if request.method =='POST' and 'opcion' in request.POST:
				opcion = request.POST['opcion']
				if opcion == 'si': # opcion=si
					# Confirma la desincripcion
					ins.delete() # Borramos la inscripcion de la DB
					# Restamos 1 al numero de "anotados" de la comision
					com.anotados = com.anotados-1
					# Actualizamos la comision
					com.save()
					# Redireccionamos a "mis_laboratorios"
					return HttpResponseRedirect(reverse('laboratorio:mis_laboratorios'))
		else:
		# NO es POST
			# Redireccionamos a 'home'
			return HttpResponseRedirect(reverse('laboratorio:detalle_laboratorio', args=[lab.slug]))
		return render (request, 'inscripcion/borrar_confirmar.html', context)
	else:
	# NO es alumno
		# Redireccionamos al home
		return HttpResponseRedirect(reverse('home'))


# Vista para mostrar el listado de inscriptos por comision
def Detalle_Comision(request, laboratorio_slug, comision_id):
	# Verificamos que el metodo se POST
	if request.method == 'POST':
		# Si es POST
		# Verificamos el rol del usuario
		if request.user.groups.filter(name='laboratorista').exists():
			# Si es laboratorista
			# Obtenemos la comision
			com = Comision.objects.get(id = comision_id)
			# Obtenemos el laboratorio
			lab = Laboratorio.objects.get(slug = laboratorio_slug)
			# Obtenemos las inscripciones para esa comision
			ins = Inscripcion.objects.filter(comision = com)
			if not ins:
			# Si no existen incripciones
				context = ({
					'laboratorio': lab,
					'mensaje':'No existen inscripciones para esta comision',
					})
			else:
				# Obtenemos el laboratorio
				lab = ins[0].laboratorio
				# Confirmamos asistencias
				# Verificamos si existe una consulta POST
				if request.method =='POST' and 'inscripcion' in request.POST:
					# Creamos la lista de los presentes
					inscripcion_ids = request.POST.getlist('inscripcion')
					# Recorremos la lista anterior
					for un_inscripcion_id in inscripcion_ids:
						# Obtenemos la inscripcion en cada iteracion
						inscripcion = ins.get(id=un_inscripcion_id)
						# Modificamso el campo de la tabla de esa inscripcion
						inscripcion.realizado = True
						# Guardamos la inscripcion
						inscripcion.save()
				# Creamos el Contexto
				context = ({
					'laboratorio': lab,
					'comision': com,
					'inscripciones': ins,
					})
			# Renderizamos el contexto
			return render (request, 'comision/detalle.html', context)
		else:
		# No es laboratorista
			# Redireccionamos al Home
			return HttpResponseRedirect(reverse('home'))
	else:
	# No es POST
		# Redireccionamos al Home
		return HttpResponseRedirect(reverse('home'))

	return render (request, 'comision/detalle.html')


# Confirmacion de la eliminacion de la comision y envio de E-Mails
def Eliminar_Comision(request, laboratorio_slug, comision_id):
	# Verificamos que el metodo se POST
	if request.method == 'POST':
		# Si es POST
		# Verificamos el rol del usuario
		if request.user.groups.filter(name='laboratorista').exists():
			# Si es laboratorista
			# Obtenemos la comision
			com = Comision.objects.get(id = comision_id)
			# Obtenemos el laboratorio
			lab = Laboratorio.objects.get(slug = laboratorio_slug)
			# Obtenemos las inscripciones para esa comision
			ins = Inscripcion.objects.filter(comision = com)
			anotados = ins.count() # Cantidad de inscripcion
			if not ins:
			# Si no existen incripciones
				context = ({
					'mensaje':'No existen inscripciones. No se enviara ningun E-Mail.',
					})
				# Verificamos si existe la consulta en el method POST
				if request.method == 'POST' and 'confirmacion' in request.POST:
					# Obtenemos la confirmacion
					confirmacion = request.POST['confirmacion']
					# Si confirmacion es si
					if confirmacion == 'si':
						# Borramos la comision
						com.delete()
						return HttpResponseRedirect(reverse('laboratorio:detalle_laboratorio', args=[lab.slug]))
			else:
				# Obtenemos el laboratorio
				mensaje = 'La comisión de %s a las %s para el laboratorio %s, ha sido cancelada, por favor inscribase en otro horario' % (com.fecha, com.horario.hora_inicio, lab.nombre)
				asunto = 'Cancelación de Laboratorio'
				# Verificamos si existe una consulta POST
				if request.method =='POST' and 'confirmacion' in request.POST:
					# Obtenemos la confirmacion
					confirmacion = request.POST['confirmacion']
					# Si confirmacion es SI
					if confirmacion == 'si':
						# Recorremos la lista de inscripciones
						for una_inscripcion in ins:
							# Armamos el E-Mail
							email = EmailMessage(asunto, mensaje, to=[una_inscripcion.alumno.user.email])
							# Enviamos el E-Mail
							email.send()
							# Borramos la inscripcion
							una_inscripcion.delete()
						# Borramos al comision
						com.delete()
						return HttpResponseRedirect(reverse('laboratorio:detalle_laboratorio', args=[lab.slug]))
				# Creamos el Contexto
				context = ({
					'email_mensaje':mensaje,
					'anotados':anotados,
					'laboratorio': lab,
					'comision': com,
					'inscripciones': ins,
					})
			# Renderizamos el contexto
			return render (request, 'comision/eliminacion_detalle.html', context)
		else:
		# No es laboratorista
			# Redireccionamos al Home
			return HttpResponseRedirect(reverse('home'))
	else:
	# No es POST
		# Redireccionamos al Home
		return HttpResponseRedirect(reverse('home'))

	return render (request, 'comision/eliminacion_detalle.html')



# Vist generica para Crear un laboratorio
class Crear_Laboratorio(CreateView):

	template_name = 'laboratorio/crear.html'
	model = Laboratorio
	success_url = reverse_lazy('laboratorio:crear_laboratorio')
	fields = ['materia', 'numero', 'nombre', 'tema', 'objetivos', 'descripcion', 'fecha_inicio', 'fecha_fin', 'cupo', 'archivo']


# Funcion de creacion de un horario y sus comisiones
def Crear_Horario(request):

	# Consultamos si el User pertenece al grupo "laboratorista"
	if request.user.groups.filter(name='laboratorista').exists():
		# Si es "laboratorista"
		# Verificamos que el methodo sea POST
		if request.method == 'POST':
			# Si el methodo es POST:
			# Obtenemos el formulario
			form = Fomulario_Crear_Horario(request.POST)
			# Verificamos si el Formulario es valido
			if form.is_valid():
				# Si es valido:
				# Instaciamos el modelo Horario:
				h = Horario(
							materia = form.cleaned_data['materia'],
							encargado = form.cleaned_data['encargado'],
							dia_semana = form.cleaned_data['dia_semana'],
							hora_inicio = form.cleaned_data['hora_inicio'],
							hora_fin = form.cleaned_data['hora_fin'],
							aula = form.cleaned_data['aula'],
							)
				# Guardamos el Horario
				h.save()
				# Una vez creado el Horario, creamos las comisiones para ese horario
				# Obtengo las fechas limites para crear las comisiones
				fecha = form.cleaned_data['fecha_inicio']
				fechahasta = form.cleaned_data['fecha_fin']
				# Obtengo el dia de la semana para ese horarios[0:lunes, 1:martes, etc..]
				weekday = WeekDay.objects.get(nombre=form.cleaned_data['dia_semana'])
				# Realizo un recursivo que recorre todas las fechas entre FECHADESDE hasta FECHAHASTA
				while fecha <= fechahasta:
					# Verifica si el weekday de esa fecha es el mismo que el del horario
					if datetime.weekday(fecha) == weekday.numero:
						# Si es el mismo, crea la comision con esa fecha
						c = Comision(
									fecha = fecha,
									horario = h,
									)
						# Guardamos la comison
						c.save()
					# Sumamos 1 dia a la fecha
					fecha = fecha + timedelta(days=1)

				# Retornamos el formulrio para crear otro horario
				return HttpResponseRedirect(reverse('laboratorio:crear_horario'))

		else:
			form = Fomulario_Crear_Horario()

		context =({
					'formulario': form,
					})

		return render (request, 'horario/crear.html', context)
	else:
	# No es laboratorista
		# Redireccionamos al Home
		return HttpResponseRedirect(reverse('home'))


# Funcion para borrar los horarios entre 2 fechas y mandar el email a todos los inscriptos
def Borrar_Horario(request):

	# Consultamos si el User pertenece al grupo "laboratorista"
	if request.user.groups.filter(name='laboratorista').exists():
		# Si es "laboratorista"
		# Verificamos si el methodo es POST
		if request.method == 'POST':
			# Si el methodo es POST:
			# Obtenemos el formulario
			form = Formulario_Borrar_Horario(request.POST)
			# Verificamos si el Formulario es valido
			if form.is_valid():
				# Si es valido:
				# Obtenemos los datos del formulario
				horario = form.cleaned_data['horario']
				fechadesde = form.cleaned_data['fecha_inicio']
				fechahasta = form.cleaned_data['fecha_fin']
				# Obtenemos las comisiones del horario
				comall = Comision.objects.filter(horario=horario)
				# Excluimos de las comisiones fuera del rango de fechas
				com = comall.filter(fecha__range=(fechadesde, fechahasta))
				# Recorremos las comisiones filtradas
				for una_com in com:
					# Obtenemos los inscriptos de cada comision
					ins = Inscripcion.objects.filter(comision=una_com)
					# Recorremos las inscripciones de la comision
					for una_ins in ins:
						# Creamos los campos del email
						asunto = 'Cancelación de Laboratorio'
						mensaje = 'La comision de %s a las %s para el laboratorio %s, ha sido cancelada, por favor inscribase nuevamente' % (una_com.fecha, una_com.horario.hora_inicio, una_ins.laboratorio.nombre)
						# Obtenemos el e-mail de cada alumno inscripto
						email = una_ins.alumno.user.email
						# Armamos el email
						email = EmailMessage(asunto, mensaje, to=[email])
						# Enviamso el email
						email.send()
						# Borramos la inscripcion
						una_inscripcion.delete()
					# Borramos la comision
					una_com.delete()
				# Retornamos el formulrio para crear otro horario
				return HttpResponseRedirect(reverse('laboratorio:crear_horario'))
		else: # if request.method == 'POST':
			form = Formulario_Borrar_Horario()
		context =({
			'formulario': form,
			})
		return render (request, 'horario/borrar.html', context)
	else:
	# No es laboratorista
		# Redireccionamos al Home
		return HttpResponseRedirect(reverse('home'))





























































#Funcion de Vista para imprimir informe de asistencias
def Pdf_Informe_Asistencia(request, comision_id):

	# Obtenemos los datos a mostrar
	# Comision
	com = Comision.objects.get(id = comision_id)
	# Lista de inscriptos en la comision
	ins = Inscripcion.objects.filter(comision = com)
	# Obtenemos la fecha del dia, en forma de string
	hoy = '0%s/0%s/%s' % (datetime.now().day, datetime.now().month, datetime.now().year)
	# Obtenemos las dimensiones de la hoja A4
	width, height = A4
	# Inicializamos el array para el pdf
	data = []

	# Indicamos el tipo de contenido a devolver, en este caso un pdf
	response = HttpResponse(content_type='application/pdf')
	# Asignamos un nombre al PDF
	response['Content-Disposition'] = 'attachement; filename=Reporte.pdf'
	# La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
	buffer = BytesIO()
	c = canvas.Canvas(buffer, pagesize=A4) # Guardamso el canvas para hojas A4 en una variable c

	# PDF: Header
	c.setLineWidth(.3)
	# Titulo
	c.setFont('Courier-Bold', 12)
	c.drawString(85,780,'FisicaWeb') # (X,Y,'lo que escribe')
	# Subtitulo
	c.setFont('Courier', 10)
	c.drawString(430,780,'Reporte:')
	# Fecha
	c.setFont('Courier', 10)
	c.drawString(480,780,hoy)
	# Linea para separar header de body
	c.line(0,775,height,775) # (X0,Y0,XF,YF)

	# PDF: Body - Head
	# Titulo del reporte
	c.setFont('Courier', 16)
	c.drawString(130,750,'Informe de asistencias al Laboratorio')
	# Informacion de la comision
	c.setFont('Courier-Bold',12)
	c.drawString(85,725,'Laboratorio:')
	c.drawString(85,710,'Fecha:')
	c.drawString(85,695,'Horario:')
	c.drawString(85,680,'Encargado:')
	# 
	c.setFont('Courier',12)
	c.drawString(180,725,'%s' %(ins[0].laboratorio.nombre))
	c.drawString(180,710,'%s, %s de %s de %s' % (com.fecha.strftime('%A'), com.fecha.day, com.fecha.month, com.fecha.year))
	c.drawString(180,695,'%s a %s' %(com.hora_inicio, com.hora_fin))
	c.drawString(180,680,'%s' %(com.encargado))

	#PDF: Body informacion
	# Tabla
	# Tabla: Headers formato
	style = getSampleStyleSheet()
	styleHT = style["Normal"]
	styleHT.alignment = TA_CENTER
	styleHT.fontSize = 14
	#Tabla: Header informacion
	legajo = Paragraph(' ''Legajo'' ',styleHT)
	apellido = Paragraph(' ''Apellido'' ',styleHT)
	nombre = Paragraph(' ''Nombre'' ',styleHT)
	asistencia = Paragraph(' ''Asistencia'' ',styleHT)
	# Agregamos el HeadTable al array
	data.append([legajo, apellido, nombre, asistencia])
	#Tabla: Body
	#Tabla: Body formato
	style = getSampleStyleSheet()
	styleBT = style["BodyText"]
	styleBT.alignment = TA_CENTER
	styleBT.fontSize = 12
	#Tabla: Body informacion
	high = 632
	for una_ins in ins:
		esta_ins = [
					una_ins.alumno.legajo,
					una_ins.alumno.user.last_name,
					una_ins.alumno.user.first_name,
					una_ins.realizado,
					]
		data.append(esta_ins)
		high = high - 18
	# Tabla: Tamaño
	width, height = A4
	table = Table(data, colWidths=[2.5 * cm, 3.5 * cm, 3.5 * cm, 3 * cm])
	table.setStyle(TableStyle([ # Estilos de la tabla
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('BOX', (0, 0), (-1, -1), 0.50, colors.black),
		]))

	# Tabla ubicacion
	table.wrapOn(c, width, height)
	table.drawOn(c, 80, high)
	c.showPage

	# PDF: Body Footer
	c.setFont('Courier',2)
	c.drawString(405,60,'FisicaWebInformeLabortorioFisicaWebInformeLabortorioFisicaWebInformeLabortorioFisicaWebInformeLabortorio')
	c.setFont('Courier',10)
	c.drawString(410,50,'Firma del encargado')
	# PDF: Footer
	c.setFont('Courier',8)
	c.drawString(200,29,'Informe generado automaticamente por el sistema de laboratorios de FisicaWeb')

	# Guardamos todo
	c.save()
	pdf = buffer.getvalue()		# Obtenemos el valor del buffer
	buffer.close()				# Cerramos el buffer
	response.write(pdf)			# Escribimos el PDF en el response
	return response

#Funcion de Vista para imprimir la lista de laboratorios
def Generar_Pdf(request):

	#Indicamos el tipo de contenido a devolver, en este caso un pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachement; filename=Reporte.pdf'
	#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
	buffer = BytesIO()
	c = canvas.Canvas(buffer, pagesize=A4) # Guardamso el canvas para hojas A4 en una variable c

	# Obtenemos la fecha del dia
	hoy = '%s / %s / %s' % (datetime.now().day, datetime.now().month, datetime.now().year)
	# PDF: Header
	c.setLineWidth(.3)
	# Titulo
	c.setFont('Helvetica', 22)
	c.drawString(30,750,'FisicaWeb') # (X,Y,'lo que escribe')
	# Subtitulo
	c.setFont('Helvetica', 12)
	c.drawString(30,735,'Reporte')
	# Fecha
	c.setFont('Helvetica-Bold', 12)
	c.drawString(480,750,hoy)
	# Linea para subrayar al fecha
	c.line(460,747,560,747) # (X0,Y0,XF,YF)

	# PDF: Body
	# Datos para imprimir

	laboratorios = Laboratorio.objects.all()

	# Tabla
	# Tabla: Headers
	style = getSampleStyleSheet()
	styleBH = style["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 10

	numero = Paragraph(' ''#'' ',styleBH)
	alumno = Paragraph(' ''Nombre'' ',styleBH)
	b1 = Paragraph(' ''Fecha de Inicio'' ',styleBH)
	b2 = Paragraph(' ''Fecha de Cierre'' ',styleBH)
	b3 = Paragraph(' ''Cupos'' ',styleBH)

	data = [] # Inicializamos la lista madre

	data.append([numero, alumno, b1, b2, b3])

	# Tabla: Body
	styleN = style["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 7

	high = 650
	for un_laboratorio in laboratorios:
		este_laboratorio = [
							un_laboratorio.numero,
							un_laboratorio.nombre,
							un_laboratorio.fecha_inicio,
							un_laboratorio.fecha_fin,
							un_laboratorio.cupo,
							]
		data.append(este_laboratorio)
		high = high - 18

	# Tabla: Tamaño
	width, height = A4
	table = Table(data, colWidths=[0.5 * cm, 7 * cm, 2.2 * cm, 2.2 * cm, 1.5 * cm])
	table.setStyle(TableStyle([ # Estilos de la tabla
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black),
		]))

	# PEF: Tamaño
	table.wrapOn(c, width, height)
	table.drawOn(c, 30, high)
	c.showPage

	c.save()
	pdf = buffer.getvalue()		# Obtenemos el valor del buffer
	buffer.close()				# Cerramos el buffer
	response.write(pdf)			# Escribimos el PDF en el response
	return response
# -*- coding: utf-8 -*-
from __future__						import unicode_literals

from django.http					import HttpResponseRedirect, HttpResponse
from django.shortcuts				import render, get_list_or_404, get_object_or_404
from django.urls					import reverse, reverse_lazy
from django.views.generic			import ListView, DetailView, CreateView, DeleteView
from itertools						import chain


from Apps.catedras.models			import (
											Carrera,
											Materia,
											Profesor,
											ComisionCatedra,
											Curso,
											Cursando,
											)


# Funcion de Vista para enlistar las materias
def Listar_Materias(request):

	# Consultamos si el User pertenece al grupo "docente"
	if request.user.groups.filter(name='docente').exists():
		# Si es "docente"
		# Redireccionamos al "Home"
		return HttpResponseRedirect(reverse('home'))
	else:
		# Si no es Docente, enlistamos todos las materias
		mat = Materia.objects.all()

	# Creamos el contexto
	context =({
		'materias': mat,
		})

	# Renderizamos el contexto
	return render (request, 'materias/lista.html', context)


# Enlistamos las comisiones por especialidad y por materia
class Lista_de_Comisiones(ListView):

	template_name = 'comisioncatedra/lista.html'
	model = ComisionCatedra
	context_object_name = 'comisiones'

	def get_context_data(self, **kwargs):
		context = super(Lista_de_Comisiones, self).get_context_data(**kwargs)

		# Clasificamos las comisiones por especialidad
		civil = ComisionCatedra.objects.filter(especialidad = 'civil').order_by(materia)
		electrica = ComisionCatedra.objects.filter(especialidad = 'electrica').order_by(materia)
		industrial = ComisionCatedra.objects.filter(especialidad = 'industrial').order_by(materia)
		mecanica = ComisionCatedra.objects.filter(especialidad = 'mecanica').order_by(materia)
		quimica = ComisionCatedra.objects.filter(especialidad = 'quimica').order_by(materia)
		sistemas = ComisionCatedra.objects.filter(especialidad = 'sistemas de informacion').order_by(materia)

		# Armamos el contexxto
		context['civil']=civil
		context['electrica']=electrica
		context['industrial']=industrial
		context['mecanica']=mecanica
		context['quimica']=quimica
		context['sistemas']=sistemas

		return context


def Lista_de_Profesores(request):

	mat = Materia.objects.all()
	if request.method == 'GET' and 'apellido' in request.GET:
		# Si existe
		# Obtenemos los valores
		apellido = request.GET['apellido']
		nombre = request.GET['nombre']
		materia_id = request.GET['materia']
		# Filtramos por apellido	/////////////////////////////////////////////////////////////////////////
		if apellido == '':
			# Si el apellido es vacio, no filtramos
			prof_apellido = Profesor.objects.all()
		else:
			# Si el apellido exite, obtenemos todos los profesores que contengan el string
			prof_apellido = Profesor.objects.filter(apellido__icontains = apellido)
		# Filtramos por nombre		/////////////////////////////////////////////////////////////////////////
		if nombre == '':
			# Si el nombre es vacio, no filtramos
			prof_nombre = prof_apellido
		else:
			# Si el nombre exite, obtenemos todos los profesores que contengan el string
			prof_nombre = prof_apellido.filter(nombre__icontains = nombre)
		# Filtrar por materia		/////////////////////////////////////////////////////////////////////////
		if materia_id == '':
			# Si la materia es vacio, no filtramos
			prof = prof_nombre
		else:
			# Si la materia exite, obtenemos la materia
			materia = Materia.objects.get(id = materia_id)
			# Obtenemos todos los profesores que esten en esa materia
			prof = prof_nombre.filter(materia = materia)
	else:
		# Si no existe
		# Mostramos todos los Profesores
		prof = Profesor.objects.all()

	context =({
		'docentes': prof,
		'materias': mat,
		})

	return render (request, 'profesores/lista.html', context)


def Detalle_Profesor(request, legajo):

	# Verificamos que el metodo se GET
	if request.method == 'GET':
		# Si es GET
		prof = Profesor.objects.get(legajo = legajo)
		# Obtenemos lo cursos donde actua el docente, segun su rango
		cursos_titular = Curso.objects.filter(titular = prof)
		cursos_adjunto = Curso.objects.filter(adjunto = prof)
		cursos_jtp = Curso.objects.filter(jtp = prof)
		cursos_ayudante = Curso.objects.filter(ayudante = prof)
		cursos = sorted(chain(cursos_titular, cursos_ayudante, cursos_adjunto, cursos_jtp))


	context =({
		'docente': prof,
		'cursos': cursos,
		})

	return render (request, 'profesores/detalle.html', context)


def Lista_de_Comisiones(request):

	especialidades = Carrera.objects.all()

	if request.method == 'GET' and 'nivel' in request.GET:
		# Si existe
		# Obtenemos los valores
		nivel = request.GET['nivel']
		carrera_id = request.GET['especialidad']
		# Filtramos por apellido	//////////////////////////////////////////////////////////////////////////
		if nivel == '':
			filtro = "si"
			nivel_carrera = "todos los años"
			# Si el apellido es vacio, no filtramos
			comisiones_nivel = ComisionCatedra.objects.all()
		else:
			filtro = "si"
			nivel_carrera = "%s° año " % (nivel)
			# Si el apellido exite, obtenemos todos los profesores que contengan el string
			comisiones_nivel = ComisionCatedra.objects.filter(nivel = nivel)
		# Filtramos por nombre		//////////////////////////////////////////////////////////////////////////
		if carrera_id == '':
			esp = "todas las carreras"
			# Si el nombre es vacio, no filtramos
			comisiones = comisiones_nivel
		else:
			# Obtenemos la escpecialidad del id
			especialidad = Carrera.objects.get(pk = carrera_id)
			esp = "Ingenieria %s" % (especialidad)
			# Si el nombre exite, obtenemos todos los profesores que contengan el string
			comisiones = comisiones_nivel.filter(carrera = especialidad)
	else:
		# Si no existe
		# Mostramos todos los Profesores
		filtro = "no"
		nivel_carrera = ""
		esp = ""
		comisiones = ComisionCatedra.objects.all()

	context =({
		'filtro': filtro,
		'nivel': nivel_carrera,
		'especialidad': esp,
		'comisiones': comisiones,
		'especialidades': especialidades,
		})

	return render (request, 'comisioncatedra/lista.html', context)


def Detalle_de_Comision(request, comision_id):

	comision = ComisionCatedra.objects.get(id = comision_id)
	cursos = Curso.objects.filter(comisioncatedra = comision)

	context =({
		'cursos':cursos,
		'comision': comision,
		})

	return render (request, 'comisioncatedra/detalle.html', context)


def Detalle_de_Curso(request, comision_id, materia_slug):

	materia = Materia.objects.get(slug = materia_slug)
	comision = ComisionCatedra.objects.get(id = comision_id)

	context = ({
		'materia': materia,
		'comision':comision,
		})
	return render(request, 'curso/detalle.html', context)
# -*- coding: utf-8 -*-
from __future__							import unicode_literals

from datetime							import datetime
from django.contrib.auth				import authenticate, login, logout
from django.contrib.auth.models			import User, Group
from django.core.mail.backends.smtp		import EmailBackend
from django.core.mail					import EmailMultiAlternatives, EmailMessage
from django.http						import HttpResponseRedirect, HttpResponse
from django.shortcuts					import render, render_to_response
from django.template					import RequestContext
from django.urls						import reverse, reverse_lazy
from django.views.defaults				import page_not_found, server_error

from Apps.usuarios.forms				import (
												Formulario_de_Contacto,
												Fomulario_Creacion_Alumno,
												)
from Apps.usuarios.models				import (
												Alumno,
												Docente,
												)



# Create your views here.

def holamundo(request):
	return render (request, 'hola.html')



def Contacto_Email(request):

	if request.method == 'POST':
		formulario = Formulario_de_Contacto(request.POST)
		if formulario.is_valid():
			asunto = 'Este mensaje es de mi pagina en Django'
			mensaje = formulario.cleaned_data['mensaje']
			email = EmailMessage(asunto, mensaje, to=['jorge.ronconi@gmail.com'])
			email.send()
		return HttpResponseRedirect(reverse('home'))

	else:
		formulario = Formulario_de_Contacto()

	return render (request, 'contacto.html', {'formulario': formulario})


# Error 404
def Error_404(request):
	return page_not_found(request, template_name='error/404.html')


# Error 500
def Error_500(request):
	return server_error(request, template_name='error/500.html')


# Enlistar y filtrar alumnos.
def Listar_Alumno(request):

	# Consultamos si el User pertenece al grupo "laboratorista"
	if request.user.groups.filter(name='laboratorista').exists():
		# Si es "laboratorista"
		# Verificamosque exista el request
		if request.method == 'GET' and 'apellido' in request.GET:
			# Si existe
			# Obtenemos los valores
			apellido = request.GET['apellido']
			nombre = request.GET['nombre']
			dni = request.GET['dni']
			legajo = request.GET['legajo']

			# Filtramos por apellido	//////////////////////////////////////////////////////////////////////////
			if apellido == '':
				# Si el apellido es vacio, no filtramos
				alu_apellido = Alumno.objects.all()
			else:
				# Si el apellido exite, obtenemos todos los usuarios que contengan el string
				alu_user = User.objects.filter(last_name__icontains = apellido)
				# Obtenemos los alumnos de esos usuarios
				alu_apellido = Alumno.objects.filter(user__in= alu_user)
			# Filtramos por nombre		//////////////////////////////////////////////////////////////////////////
			if nombre == '':
				# Si el nombre es vacio, no filtramos
				alu_nombre = alu_apellido
			else:
				# Si el nombre exite, obtenemos todos los usuarios que contengan el string
				alu_user = User.objects.filter(first_name__icontains = nombre)
				# Obtenemos los alumnos de esos usuarios
				alu_nombre = alu_apellido.filter(user__in= alu_user)
			# Filtramos por dni			//////////////////////////////////////////////////////////////////////////
			if dni == '':
				# Si el dni es vacio, no filtramos
				alu_dni = alu_nombre
			else:
				# Obtenemos los alumnos de esos usuarios
				alu_dni = alu_nombre.filter(dni__icontains= dni)
			# Filtramos por legajo		///////////////////////////////////////////////////////////////////////////
			if legajo == '':
				# Si el legajo es vacio, no filtramos
				alu = alu_dni
			else:
				# Obtenemos los alumnos de esos usuarios
				alu = alu_dni.filter(legajo__icontains = legajo)

		else:
			# Si no existe
			# Mostramos todas los alumnos
			alu = Alumno.objects.all()

		context =({
			'alumnos': alu,
		})

		return render (request, 'alumno/lista.html', context)

	# Si no es laboratorista
	else:
		# Redireccionamos al "Home"
		return HttpResponseRedirect(reverse('home'))


# Funcion para que el laboratorista cree un usuario:alumno
def Crear_Alumno(request):

	# Consultamos si el User pertenece al grupo "laboratorista"
	if request.user.groups.filter(name='laboratorista').exists():
		# Si es "laboratorista"
		# Verificamos que el methodo sea POST
		if request.method == 'POST':
			# Si el methodo es POST:
			# Obtenemos el formulario
			form = Fomulario_Creacion_Alumno(request.POST)
			# Verificamos si el Formulario es valido
			if form.is_valid():
				# Si es valido:
				# Obtenemos el Grupo alumnos
				grupo_alumno = Group.objects.get(name='alumno')
				# instanciamos los modelos
				# Creamos el User de Django
				u = User.objects.create_user(
											username = form.cleaned_data['nickname'],
											email = form.cleaned_data['email'],
											password = form.cleaned_data['password1'],
											last_name = form.cleaned_data['apellido'],
											first_name = form.cleaned_data['nombre'],
											)
				# Lo agregamos al grupo alumnos
				u.groups.add(grupo_alumno)
				# Instanciamos a usuarios.Alumno
				a = Alumno(
					user = u,
					fecha_nacimiento = form.cleaned_data['fecha_nacimiento'],
					dni = form.cleaned_data['dni'],
					legajo = form.cleaned_data['legajo'],
					#comision = form.cleaned_data['comision'],
					carrera = form.cleaned_data['especialidad'],
					timestamp = datetime.now(),
					)
				u.save() # Guardamos Django.User
				a.save() # Guardamos usuarios.Alumno
				print (a)
				print (u)
				# Retornamos el formulrio para crear otro alumno
				return HttpResponseRedirect(reverse('usuario:crear_alumno'))
			else:
				print ('algo no anda')

		else:
			form = Fomulario_Creacion_Alumno()

		context =({
			'formulario': form,
		})

		return render (request, 'alumno/crear.html', context)

	# Si no es laboratorista
	else:
		# Redireccionamos al "Home"
		return HttpResponseRedirect(reverse('home'))
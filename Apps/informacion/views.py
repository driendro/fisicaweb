# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Publicacion, Tags

# Create your views here.

# Home muestra las ultimas 4 publicaciones
class PublicList (ListView):

	template_name = 'blog.html'
	model = Publicacion
	context_object_name = 'publicaciones'

	def get_context_data(self, **kwargs):
		context = super(PublicList, self).get_context_data(**kwargs)
		# Mostramos las ultimas 4 publicaciones
		publicaciones = Publicacion.objects.all().order_by('timestamp')[:4]
		# Consultamos si el User pertenece al grupo "docente"
		if self.request.user.groups.filter(name='docente').exists():
			# Si es "laboratorista"
			grupo = 'docente'
		else:
			# Consultamos si el User pertenece al grupo "laboratorista"
			if self.request.user.groups.filter(name='laboratorista').exists():
				# Si es "laboratorista"
				grupo = 'laboratorista'
			else:
				# Consultamos si el User pertenece al grupo "alumno"
				if self.request.user.groups.filter(name='alumno').exists():
					# Si es "alumno"
					grupo = 'alumno'
				else:
					# Si no es ninguno
					grupo = ''
		context['publicaciones'] = publicaciones
		context['grupo']= grupo
		return context


# Enlista en un template todas las publicaciones ordenadas por fecha
class Lista_Posteos(ListView):
	template_name = 'publicacion/lista.html'
	model = Publicacion
	context_object_name = 'publicaciones'

	def get_context_data(self, **kwargs):
		context = super(Lista_Posteos, self).get_context_data(**kwargs)
		# Ordenamos las publicaciones
		publicaciones = Publicacion.objects.all().order_by('timestamp')
		context['publicaciones'] = publicaciones
		return context


class PostDetail(DetailView):

	template_name = 'post_detalle.html'
	model = Publicacion
	context_object_name = 'post'

	def get_context_data(self, **kwargs):
		context = super(PostDetail, self).get_context_data(**kwargs)
		# Consultamos si el User pertenece al grupo "docente"
		if self.request.user.groups.filter(name='docente').exists():
			# Si es "laboratorista"
			grupo = 'docente'
		else:
			# Consultamos si el User pertenece al grupo "laboratorista"
			if self.request.user.groups.filter(name='laboratorista').exists():
				# Si es "laboratorista"
				grupo = 'laboratorista'
			else:
				# Consultamos si el User pertenece al grupo "alumno"
				if self.request.user.groups.filter(name='alumno').exists():
					# Si es "alumno"
					grupo = 'alumno'
				else:
					# Si no es ninguno
					grupo = ''

		context['grupo']= grupo
		return context
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from datetime							import date
from django.contrib.auth.models			import User
from django.db							import models
from django.template.defaultfilters		import slugify
from uuid								import uuid4

from Apps.usuarios.models				import(
												Alumno,
												Docente,
												)


# Funcion para guardar los docuntos
def _generar_ruta_documento(instance, filename):
	# Extraer extension del fichero
	extension = os.path.splitext(filename)[1][1:]
	# Generamos la ruta relativa a media_root
	# donde almacenar el archivo usando la fecha actual
	# año/media/dia
	ruta = os.path.join('static/media/documentos', date.today().strftime('%y/%m/%d'))
	# Generamos el nombre del archivo con un idenfiticar
	# aleatorio y la extension del archivo original
	nombre_archivo = '{}.{}'.format(uuid4().hex,extension)
	# Retornamos la ruta completa
	return os.path.join(ruta, nombre_archivo)


class Tags(models.Model):

	nombre = models.CharField(max_length=100)
	slug = models.SlugField(editable=False)
	creado_el = models.DateTimeField(auto_now_add=True, auto_now=False)

	def save(self):
		self.slug = slugify(self.nombre)
		super(Tags, self).save()

	class Meta:
		ordering = ['nombre']
		verbose_name = "Etiqueta"
		verbose_name_plural = "Etiquetas"

	def __unicode__(self): #Python 2
		return '%s' % (self.nombre)

	def __str__(self): #Python 3
		return '%s' % (self.nombre)



class Publicacion(models.Model):

	titulo = models.CharField(max_length=50)
	cuerpo = models.TextField()
	autor = models.ForeignKey(Docente)
	timestamp = models.TimeField(auto_now=False, auto_now_add=True)
	tags = models.ManyToManyField(Tags, verbose_name='Etiqueta')
	slug = models.SlugField(editable=False)

			# auto_now=False ULTIMA MODIFICACION
			# auto_now_add=True SOLO GUARDA CUANDO SE CREO

	def save(self):
		self.slug = slugify(self.titulo)
		super(Publicacion, self).save()

	class Meta:
		verbose_name = "Publicacion"
		verbose_name_plural = "Publicaciones"

	def __unicode__(self): #Python 2
		return '%s' % (self.titulo)

	def __str__(self): #Python 3
		return '%s' % (self.titulo)


class Documento(models.Model):

	nombre = models.CharField(max_length=50)
	archivo = models.FileField(upload_to=_generar_ruta_documento)
	autor = models.ForeignKey(Docente)
	descripcion = models.TextField(default='Descripcion no disponible')
	tags = models.ManyToManyField(Tags, verbose_name='Etiqueta')
	slug = models.SlugField(editable=False)
	timestamp = models.DateField(auto_now=False , auto_now_add=True)

	class Meta:
		ordering =['nombre']
		verbose_name = "Documento"
		verbose_name_plural = "Documentos"

	def save(self):
		super(Documento, self).save()

	def __unicode__(self): #Python 2
		return '%s' % (self.nombre)

	def __str__(self): #Python 3
		return '%s' % (self.nombre)
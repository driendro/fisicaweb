# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from uuid import uuid4

from Apps.choices import DIAS_SEMANA_CHOICES
from Apps.usuarios.models import Alumno, Docente
from Apps.catedras.models import Materia

def _generar_ruta_documento(instance, filename):
	# Extraer extension del fichero
	extension = os.path.splitext(filename)[1][1:]
	# Generamos la ruta relativa a media_root
	# donde almacenar el archivo usando la fecha actual
	# año/mes/dia
	ruta = os.path.join('static/media/documentos', date.today().strftime('%y/%m/%d'))
	# Generamos el nombre del archivo con un idenfiticar
	# aleatorio y la extension del archivo original
	nombre_archivo = '{}.{}'.format(uuid4().hex,extension)
	# Retornamos la ruta completa
	return os.path.join(ruta, nombre_archivo)

class Laboratorio(models.Model):

	materia = models.ForeignKey(Materia)
	numero = models.PositiveIntegerField()
	nombre = models.CharField(max_length=50)
	tema = models.CharField(max_length=50)
	objetivos = models.TextField()
	descripcion = models.TextField()
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()
	cupo = models.PositiveIntegerField(default=20)
	archivo = models.FileField(upload_to=_generar_ruta_documento, null=True, blank=True)
	slug = models.SlugField(editable=False)

	def save(self):
		self.slug = slugify(self.nombre)
		super(Laboratorio, self).save()

	class Meta:
		ordering = ['numero']
		verbose_name = "Laboratorio"
		verbose_name_plural = "Laboratorios"

	def __unicode__(self): # Python 2
		return '%s - %s' % (self.numero, self.nombre)

	def __str__(self): #P ython 3
		return '%s - %s' % (self.numero, self.nombre)


class WeekDay(models.Model):

	numero = models.PositiveIntegerField(primary_key=True)
	nombre = models.CharField(max_length=50)

	class Meta:
		ordering = ['numero']
		verbose_name = 'Día de la semana'
		verbose_name_plural = 'Días de la semana'

	def __unicode__(self): # Python 2
		return '%s' % (self.nombre)

	def __str__(self): #P ython 3
		return '%s' % (self.nombre)


class Horario(models.Model):

	materia = models.ForeignKey(Materia)
	encargado = models.ForeignKey(Docente)
	dia_semana = models.ForeignKey(WeekDay)
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	aula = models.CharField(max_length=50)
	turno = models.PositiveIntegerField(editable=False)

	def save(self):
		turno = '%s%s' % (self.dia_semana.numero, self.hora_inicio.hour)
		self.turno = turno
		super(Horario, self).save()

	class Meta:
		ordering = ['dia_semana', 'hora_inicio']
		verbose_name = "Horario"
		verbose_name_plural = "Horarios"

	def __unicode__(self): #Python 2
		return '%s: %s - %s | %s' % (self.dia_semana, self.hora_inicio, self.hora_fin, self.turno)

	def __str__(self): #Python 3
		return '%s: %s - %s | %s' % (self.dia_semana, self.hora_inicio, self.hora_fin, self.turno)


class Comision(models.Model):

	fecha = models.DateField()
	horario = models.ForeignKey(Horario)
	turno = models.PositiveIntegerField(editable=False)
	anotados = models.PositiveIntegerField(editable=False, default=0)

	def save(self):
		turno = '%s%s' % (self.fecha.weekday(),self.horario.hora_inicio.hour)
		self.turno = turno
		super(Comision, self).save()

	class Meta:
		ordering = ['anotados','fecha']
		verbose_name = "Comision"
		verbose_name_plural = "Comisiones"

	def __unicode__(self): #Python 2
		return '%s %s: %s-%s' % (self.horario.dia_semana.nombre, self.fecha, self.horario.hora_inicio, self.horario.hora_fin)

	def __str__(self): #Python 3
		return '%s %s: %s-%s' % (self.horario.dia_semana.nombre, self.fecha, self.horario.hora_inicio, self.horario.hora_fin)


class Inscripcion(models.Model):

	alumno = models.ForeignKey(Alumno)
	comision = models.ForeignKey(Comision)
	laboratorio = models.ForeignKey(Laboratorio)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	realizado = models.BooleanField(editable=False, default=False)

	class Meta:
		verbose_name = "Inscripcion"
		verbose_name_plural = "Inscripciones"
		# unique_together = (("alumno", "laboratorio"),)

	def __unicode__(self): #Python 2
		return '%s - %s: %s' % (self.alumno, self.comision.fecha.weekday(), self.comision.fecha)

	def __str__(self): #Python 3
		return '%s - %s: %s' % (self.alumno, self.comision.fecha.weekday(), self.comision.fecha)
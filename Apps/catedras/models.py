# -*- coding: utf-8 -*-
from __future__ 							import unicode_literals

from django.db 								import models
from django.template.defaultfilters 		import slugify

#from Apps.usuarios.models					import Alumno, Docente


class Carrera(models.Model):
	nombre = models.CharField(max_length=50)
	slug = models.SlugField(editable=False)

	def save(self):
		self.slug = slugify(self.nombre)
		super(Carrera, self).save()

	class Meta:
		ordering = ['nombre']
		verbose_name = 'Carrera'
		verbose_name_plural = 'Carreras'

	def __unicode__(self): #Python 2
		return '%s' % (self.nombre)

	def __str__(self): #Python 3
		return '%s' % (self.nombre)


class Materia(models.Model):
	nombre = models.CharField(max_length=10)
	slug = models.SlugField(editable=False)

	def save(self):
		self.slug = slugify(self.nombre)
		super(Materia, self).save()

	class Meta:
		ordering = ['nombre']
		verbose_name = 'Materia'
		verbose_name_plural = 'Materias'

	def __unicode__(self): # Python 2
		return '%s' % (self.nombre)

	def __str__(self): # Python 3
		return '%s' % (self.nombre)

# Es para Testeo, es valido para crear las comisiones
class Profesor(models.Model):
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	legajo = models.PositiveIntegerField(blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	materia = models.ManyToManyField('Materia', blank=True)

	class Meta:
		ordering = ['apellido']
		verbose_name='Profesor'
		verbose_name_plural='Profesores'

	def __unicode__(self): #Python 2
		return '%s, %s' % (self.apellido, self.nombre)

	def __str__(self): #Python 3
		return '%s, %s' % (self.apellido, self.nombre)
# Termina clase test


class ComisionCatedra(models.Model):
	numero = models.PositiveIntegerField()
	carrera = models.ForeignKey(Carrera)
	nivel = models.PositiveIntegerField()

	class Meta:
		ordering = ['carrera','numero']
		verbose_name = "Comision"
		verbose_name_plural = "Comisiones"

	def __unicode__(self): #Python 2
		return '%s - %s' % (self.carrera, self.numero)

	def __str__(self): #Python 3
		return '%s - %s' % (self.carrera, self.numero)


class Curso(models.Model):
	comisioncatedra = models.ForeignKey(ComisionCatedra)
	materia = models.ForeignKey(Materia)
	titular = models.ManyToManyField('Profesor', related_name='titular',blank=True)
	adjunto = models.ManyToManyField('Profesor', related_name='adjunto',blank=True)
	jtp = models.ManyToManyField('Profesor', related_name='jtp',blank=True)
	ayudante = models.ManyToManyField('Profesor', related_name='ayudante',blank=True)

	class Meta:
		ordering = ['comisioncatedra','materia']
		verbose_name = "Curso"
		verbose_name_plural = "Cursos"

	def __unicode__(self): #Python 2
		return '%s - %s' % (self.comisioncatedra, self.materia)

	def __str__(self): #Python 3
		return '%s - %s' % (self.comisioncatedra, self.materia)


class Cursando(models.Model):
	alumno = models.ForeignKey('usuarios.Alumno',blank=True, null=True)
	curso = models.ForeignKey(Curso)
	ciclo = models.PositiveIntegerField()


	class Meta:
		verbose_name = "Cursada"
		verbose_name_plural = "Cursadas"

	def __unicode__(self): #Python 2
		return '%s - %s' % (self.alumno, self.curso)

	def __str__(self): #Python 3
		return '%s - %s' % (self.alumno, self.curso)
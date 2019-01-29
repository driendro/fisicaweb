# -*- coding: utf-8 -*-
from __future__ 						import unicode_literals

from django.db 							import models
from django.contrib.auth.models 		import User

from Apps.catedras.models 				import Carrera


class Alumno(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	fecha_nacimiento = models.DateField()
	dni = models.PositiveIntegerField()
	legajo = models.CharField(max_length=5)
	carrera = models.ForeignKey(Carrera)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		verbose_name = "Alumno"
		verbose_name_plural = "Alumnos"

	def __unicode__(self): # Python 2
		return '%s, %s' % (self.user.last_name, self.user.first_name)

	def __str__(self): # Python 3
		return '%s, %s' % (self.user.last_name, self.user.first_name)


class Docente(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	legajo = models.PositiveIntegerField(null=True, blank=True)
	dni = models.PositiveIntegerField()

	class Meta:
		verbose_name = "Docente"
		verbose_name_plural = "Docentes"

	def __unicode__(self): # Python 2
		return '%s, %s' % (self.user.last_name, self.user.first_name)

	def __str__(self): # Python 3
		return '%s, %s' % (self.user.last_name, self.user.first_name)
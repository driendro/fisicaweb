# -*- coding: utf-8 -*-

from datetime							import datetime, timedelta
from django								import forms
from django.contrib.admin				import widgets
from django.contrib.auth.models			import User

from Apps.catedras.models				import (
												Materia,
												)
from Apps.usuarios.models				import (
												Alumno,
												Docente,
												)
from Apps.laboratorio.models			import (
												Laboratorio,
												Comision,
												Inscripcion,
												Horario,
												WeekDay,
												)


# Formulario para Crear el horario y sus comisiones
class Fomulario_Crear_Horario(forms.Form):

	materia = forms.ModelChoiceField(label='Materia', queryset=Materia.objects.all())
	dia_semana = forms.ModelChoiceField(label='Día de la semana', queryset=WeekDay.objects.all())
	hora_inicio = forms.TimeField(label='Hora de inicio (Ej. 18:30)')
	hora_fin = forms.TimeField(label='Hora de finalizacion (Ej. 20:30)')
	encargado = forms.ModelChoiceField(label='Encargado del turno', queryset=Docente.objects.all())
	aula = forms.CharField(label='Aula')
	fecha_inicio = forms.DateField(label='Desde', initial='%s' %(datetime.now().strftime("1/03/%Y")))
	fecha_fin = forms.DateField(label='Hasta', initial='%s' %(datetime.now().strftime("1/12/%Y")))

	def clean(self):
		# Limpiamos los datos del formulario
		cleaned_data = super(Fomulario_Crear_Horario, self).clean()
		# Retornamos la info limpia
		return cleaned_data


# Formulario para borrar las comisiones de un horario entre fechas
class Formulario_Borrar_Horario(forms.Form):

	horario = forms.ModelChoiceField(label='Horario', queryset=Horario.objects.all())
	fecha_inicio = forms.DateField(label='Desde', initial='%s' %((datetime.now()+timedelta(days=1)).strftime("%d/%m/%Y")))
	fecha_fin = forms.DateField(label='Hasta', initial='%s' %(datetime.now().strftime("1/12/%Y")))

	def clean(self):
		# Limpiamos los datos del formulario
		cleaned_data = super(Formulario_Borrar_Horario, self).clean()

		# Verificamos que la fecha de inicio no halla pasado
		# Verificamos en primer lugar el año
		if cleaned_data.get('fecha_inicio').strftime("%Y") == datetime.now().strftime("%Y"):
			# Si los años son iguales, comparamos los meses
			if cleaned_data.get('fecha_inicio').strftime("%m") == datetime.now().strftime("%m"):
				# Si los meses son iguales, comparamos los dias
				if cleaned_data.get('fecha_inicio').strftime("%d") == datetime.now().strftime("%d"):
					# Si los dias son iguales devolvemos el error
					raise forms.ValidationError('Se intenta borrar una comision que ya fue realizada, cambie la fecha "Desde"')
				else:
					# Si el dia es menor
					if cleaned_data.get('fecha_inicio').strftime("%d") < datetime.now().strftime("%d"):
						# Devolvemos el error
						raise forms.ValidationError('Se intenta borrar una comision que ya fue realizada, cambie la fecha "Desde"')
			else:
				# Si el mes es menor
				if cleaned_data.get('fecha_inicio').strftime("%m") < datetime.now().strftime("%m"):
					# Devolvemos el error
					raise forms.ValidationError('Se intenta borrar una comision que ya fue realizada, cambie la fecha "Desde"')
		else:
			# Si el año es menor
			if cleaned_data.get('fecha_inicio').strftime("%Y") < datetime.now().strftime("%Y"):
				# Devolvemos el error
				raise forms.ValidationError('Se intenta borrar una comision que ya fue realizada, cambie la fecha "Desde"')
		# Retornamos la info limpia
		return cleaned_data
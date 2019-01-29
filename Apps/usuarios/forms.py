# -*- coding: utf-8 -*-
from django								import forms
from django.contrib.admin				import widgets
from django.contrib.auth.models			import User

from Apps.choices						import(
												ESPECIALIDADES_CHOICES,
												)
from Apps.catedras.models				import (
												ComisionCatedra,
												Carrera
												)
from Apps.usuarios.models				import(
												Alumno,
												Docente,
												)


# Formulario de contacto
class Formulario_de_Contacto(forms.Form):

	correo = forms.EmailField()
	mensaje = forms.CharField()


# Formulario de creacion de un "Alumno" nuevo
class Fomulario_Creacion_Alumno(forms.Form):

	#User
	nickname = forms.CharField(label='Nombre de usuario', min_length=5)
	apellido = forms.CharField(label='Apellido')
	nombre = forms.CharField(label='Nombre')
	email = forms.EmailField(label='Direccion de E-Mail')
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), max_length=30, min_length=8)
	password2 = forms.CharField(label='Vuelva a escribir la contraseña', widget=forms.PasswordInput(), max_length=30, min_length=8)

	#Alumno
	fecha_nacimiento = forms.DateField(label='Fecha de nacimiento (Ej: 15/08/99)')
	dni = forms.IntegerField(label='DNI o Pasaporte')
	legajo = forms.IntegerField(label='Legajo', max_value=99999, min_value =10000)
	comision = forms.ModelChoiceField(label='Comision', queryset=ComisionCatedra.objects.all())
	especialidad = forms.ModelChoiceField(label='Especialidad', queryset=Carrera.objects.all())

	def clean(self):
		# Limpiamos los datos del formulario
		cleaned_data = super(Fomulario_Creacion_Alumno, self).clean()

		# Verificamos que no exista el username
		# Obtenemos el usuario del formulario
		cnickname = cleaned_data.get('nickname')
		# Verificamos que no exista el username
		if User.objects.filter(username=cnickname).exists():
			# Si existe devolvemos el error
			raise forms.ValidationError('Nombre de usuario no valido, elija otro')

		# Verificamos que el DNI y el legajo sean unicos
		# Obtenemos el dni y el legajo del formulario
		cdni = cleaned_data.get('dni')
		clegajo = cleaned_data.get('legajo')
		# Verificamos que no exista la combinacion (dni,legajo):
		if Alumno.objects.filter(dni=cdni, legajo=clegajo).exists():
			# Si existe la combinacion devolvemos el error
			raise forms.ValidationError('Ya existe un alumno duplicado')
		else:
			# Si no existe la combinacion
			# Verificamos que no exista el DNI
			if Alumno.objects.filter(dni=cdni).exists():
				# Si existe el DNI devolvemos el error
				raise forms.ValidationError('DNI o Pasaporte duplicado')
			#Verificamos que no exista el legajo
			if Alumno.objects.filter(legajo=clegajo).exists():
				# Si existe el legajo devolvemos el error
				raise forms.ValidationError('Legajo duplicado')

		# Verificamos que Password1 y Password2 sean iguales
		# Obtenemos las contraseñas
		cpassword1 = cleaned_data.get('password1')
		cpassword2 = cleaned_data.get('password2')
		# Verificamos que sean iguales
		if cpassword1 != cpassword2:
			# Si no coinciden
			raise forms.ValidationError('Las contraseñas no coinciden')

		return cleaned_data
# -*- coding: utf-8 -*-
from __future__					import unicode_literals

from django.contrib				import admin

from Apps.catedras.models		import(
										Carrera,
										Materia,
										Profesor,
										ComisionCatedra,
										Curso,
										Cursando,
										)

# Register your models here.

admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Profesor)
admin.site.register(ComisionCatedra)
admin.site.register(Curso)
admin.site.register(Cursando)
# -*- coding: utf-8 -*-
from __future__				import unicode_literals

from django.contrib			import admin
from .models				import(
									Laboratorio,
									Comision,
									Inscripcion,
									Horario,
									WeekDay,
									)

# Register your models here.

admin.site.register(Laboratorio),
admin.site.register(Comision),
admin.site.register(Inscripcion),
admin.site.register(Horario),
admin.site.register(WeekDay),
from rest_framework import serializers

from Apps.laboratorio.models		import (
											Laboratorio,
											Comision,
											Inscripcion,
											Horario,
											WeekDay,
											)

class Laboratorio_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Laboratorio
		fields = ('materia', 'numero', 'nombre', 'tema', 'objetivos', 'descripcion', 'fecha_inicio', 'fecha_fin', 'cupo', 'archivo', 'slug')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework.response import Response

from Apps.laboratorio.models		import (
											Laboratorio,
											Comision,
											Inscripcion,
											Horario,
											WeekDay,
											)

from Apps.api.serializers import Laboratorio_Serializer

@api_view(['GET', 'POST'])
def laboratorio_list(request):
	if request.method == 'GET':
		lab = Laboratorio.objects.all()
		serializer = Laboratorio_Serializer(lab, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = Laboratorio_Serializer(data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'DELETE'])
def laboratorio_details(request, pk):
	try:
		lab = Laboratorio.objects.get(pk=pk)
	except lab.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = Laboratorio_Serializer(lab)
		return Response(serializer.data)
	if request.method == 'PUT':
		serializer = Laboratorio_Serializer(lab, data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	elif request.method == 'DELETE':
		lab.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
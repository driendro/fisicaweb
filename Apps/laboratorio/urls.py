# -*- coding: utf-8 -*-
"""fisicaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.contrib import admin

from Apps.laboratorio.views import (
                                    Detalle_del_Laboratorio,        # Detallamos el laboratorio y su inscripcion
                                    Listar_Laboratorio,             # Listamos los laboratorios
                                    Mis_Laboratorios,               # Listamos los laboratorios al los que estoy inscripto
                                    Inscripcion_Laboratorio,        # Llevamos a cabo la inscripcion a la comision
                                    Cancelar_Inscripcion,           # Borramos la inscripcion
                                    Detalle_Comision,               # Inscriptos por comision
                                    Eliminar_Comision,              # Borrar comision y envio de E-Mails
                                    Crear_Laboratorio,              # Para crear un laboratorio
                                    Crear_Horario,                  # Para crear todas las comisiones del año
                                    Borrar_Horario,                 # Elimina un horario con sus comisiones

                                    # Impresiones de PDF
                                    Pdf_Informe_Asistencia,         # Imprime el infomrme de asistencias de una comision
                                    Generar_Pdf,                    # Imprime en Pdf la lista de laboratorios

                                    )

urlpatterns = [
	url(r'^mat/(?P<slug>[-\w]+)/$', login_required(Listar_Laboratorio), name='laboratorios'),
    url(r'^(?P<slug>[-\w]+)/$', login_required(Detalle_del_Laboratorio), name='detalle_laboratorio'),
    url(r'^(?P<laboratorio_id>[-\d]+)/(?P<comision_id>[-\d]+)/$', login_required(Inscripcion_Laboratorio), name='inscripcion_laboratorio'),
    url(r'^(?P<laboratorio_slug>[-\w]+)/comision/(?P<comision_id>[-\d]+)/$', login_required(Detalle_Comision), name='detalle_comision'),
    url(r'^(?P<laboratorio_slug>[-\w]+)/comision/(?P<comision_id>[-\d]+)/borrar/$', login_required(Eliminar_Comision), name='eliminar-comision'),
    url(r'^(?P<laboratorio_slug>[-\w]+)/comision/(?P<comision_id>[-\d]+)/print/$', login_required(Pdf_Informe_Asistencia), name='informe-asistencia-laboratorio'),
    url(r'^mis/laboratorios/$', login_required(Mis_Laboratorios), name='mis_laboratorios'),
    url(r'^mis/laboratorios/delete/(?P<inscripcion_id>[-\d]+)/$', login_required(Cancelar_Inscripcion), name='cancelar_inscripcion'),
    url(r'^print/lista/labs/$', login_required(Generar_Pdf), name='imprimir-laboratorio'),
    url(r'^create/new/lab/$', login_required(Crear_Laboratorio.as_view()), name='crear_laboratorio'),
    url(r'^create/new/hor/$', login_required(Crear_Horario), name='crear_horario'),
    url(r'^delete/hor/$', login_required(Borrar_Horario), name='eliminar_horario'),
]
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
from django.conf.urls               import url, include
from django.conf                    import settings
from django.conf.urls.static        import static
from django.contrib                 import admin
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views  import sitemap

from Apps.catedras.views import (
                                    Listar_Materias,                # Listamos las materias
                                    Lista_de_Profesores,            # Listamos los docentes
                                    Detalle_Profesor,               # Detalle del docente
                                    Lista_de_Comisiones,            # Listado de comisiones
                                    Detalle_de_Comision,            # Detalle de las comisiones
                                    Detalle_de_Curso,
                                    )


## /acad/
## namespace='catedras'
urlpatterns = [
	url(r'^mat/$', login_required(Listar_Materias), name='materias'),
    url(r'^prof/$', Lista_de_Profesores, name='profesores'),
    url(r'^prof/(?P<legajo>[-\d]+)$', Detalle_Profesor, name='profesor_detalle'),
    url(r'^com/$', Lista_de_Comisiones, name='comisiones'),
    url(r'^com/(?P<comision_id>[-\d]+)$', Detalle_de_Comision, name='comision_detalle'),
    url(r'^com/(?P<comision_id>[-\d]+)/(?P<materia_slug>[-\w]+)$', Detalle_de_Curso, name='curso_detalle'),
]
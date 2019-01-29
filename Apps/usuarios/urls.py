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
from django.conf                        import settings
from django.conf.urls                   import url, include, handler404, handler500
from django.conf.urls.static            import static
from django.contrib                     import admin
from django.contrib.auth.decorators     import login_required
from django.contrib.auth.views          import logout, login

from Apps.usuarios.views                import(
                                                Contacto_Email,
                                                Error_404,
                                                Error_500,
                                                Crear_Alumno,
                                                Listar_Alumno,
                                                holamundo,
                                                )

handler404 = Error_404
handler500 = Error_500

urlpatterns = [
	# Logout
	url(r'^logout/$',logout, {'template_name': 'sesion/logout.html'}, name='logout'),
	# Login
	url(r'^login/$', login, {'template_name': 'sesion/login.html'}, name='login'),
    # Contacto
    url(r'^contacto/$', Contacto_Email, name='contacto'),
    # Crear usuario Alumno
    url(r'^crear_alumno/$', Crear_Alumno, name='crear_alumno'),
    url(r'^alumnos/$', login_required(Listar_Alumno), name='administrar_alumnos'),


    url(r'^holamundo/$',holamundo),
]

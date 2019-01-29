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
from django.contrib.sitemaps.views  import sitemap

from Apps.informacion.views         import PublicList

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', PublicList.as_view(), name='home'),
    url(r'^blog/', include('Apps.informacion.urls', namespace='informacion')),
    url(r'^labs/', include('Apps.laboratorio.urls', namespace='laboratorio')),
    url(r'^user/', include('Apps.usuarios.urls', namespace='usuario')),
    url(r'^acad/', include('Apps.catedras.urls', namespace='catedras')),
    url(r'^api/', include('Apps.api.urls', namespace='api')),
    url('', include ('pwa.urls')),

]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

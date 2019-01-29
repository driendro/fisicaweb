import os, sys
import site

# PATH a donde esta el manage.py del projecto Django
sys.path.append('/var/www/scr/')
sys.path.append('/var/www/scr/fisicaweb/')

#Importante hacerlo asi, si hay varias instancias corriendo (en lugar de setdefault)
#os.environ['DJANGO_SETTINGS_MODULE']="fisicaweb.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fisicaweb.settings")

#Prevenimos UnicodeEncodeError
os.environ.setdefault("LANG","en_US.UTF-8")
os.environ.setdefault("LC_ALL","en_US.UTF-8")

#Obtenemos la aplicacion
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

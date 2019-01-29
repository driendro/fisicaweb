# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Publicacion, Tags, Documento

# Register your models here.

admin.site.register(Publicacion),
admin.site.register(Tags),
admin.site.register(Documento),
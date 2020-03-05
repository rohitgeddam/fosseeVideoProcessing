from django.contrib import admin
from api import models
# Register your models here.
admin.site.register(models.VideoModel)
admin.site.register(models.SrtModel)
admin.site.register(models.Chunk)
admin.site.register(models.FusedResult)
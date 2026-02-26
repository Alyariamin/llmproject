from django.contrib import admin
from . import models

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    exclude = ['published_at']
    list_display = ['title', 'summary','status','published_at']
    list_filter = ['tag','updated_at','status']
    filter_horizontal = ['tag']
    search_fields = ['title__istartswith']
admin.site.register(models.Tag)

@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['question','answer']

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
    list_display = ['question', 'answer']
    readonly_fields = ['question', 'answer', 'created_at', 'related_documents_display']
    exclude = ['documents']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    # Allow entering the detail page, but strip out save buttons
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_delete_link'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def related_documents_display(self, obj):
        docs = obj.documents.all()
        if not docs:
            return "No related documents"
        return ", ".join(doc.title for doc in docs)
    related_documents_display.short_description = "Related documents"
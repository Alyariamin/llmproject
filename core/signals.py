from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document
from .tasks import rebuild_index_task


@receiver([post_save, post_delete], sender=Document)
def trigger_reindex(sender, **kwargs):
    rebuild_index_task.delay()
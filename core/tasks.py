from celery import shared_task
from .services.index_service import rebuild_tfidf_index


@shared_task
def rebuild_index_task():
    rebuild_tfidf_index()
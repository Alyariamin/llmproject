import numpy as np
from django.core.cache import cache
from sklearn.feature_extraction.text import TfidfVectorizer
from ..models import Document


CACHE_KEY = "tfidf_vectors"
CACHE_TIMEOUT = 60 * 60  # 1 hour


def rebuild_tfidf_index():
    """
    Rebuild TF-IDF index and store it in cache.
    This function is meant to be called by a Celery task.
    """

    documents = Document.objects.filter(
        status=Document.STATUS_PUBLISHED
    )

    if not documents.exists():
        cache.delete(CACHE_KEY)
        return

    docs_list = list(documents)

    texts = [
        f"{doc.title} {doc.content}"
        for doc in docs_list
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    doc_vectors = tfidf_matrix.toarray()
    doc_ids = [doc.id for doc in docs_list]

    index_data = {
        "vectorizer": vectorizer,
        "doc_vectors": doc_vectors,
        "doc_ids": doc_ids,
    }

    cache.set(CACHE_KEY, index_data, timeout=CACHE_TIMEOUT)
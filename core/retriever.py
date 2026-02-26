import numpy as np
from django.core.cache import cache
from langchain_core.documents import Document as LCDocument
from langchain_core.retrievers import BaseRetriever
from .models import Document


CACHE_KEY = "tfidf_vectors"


class TFIDFRetriever(BaseRetriever):

    similarity_threshold: float = 0.1

    def _get_relevant_documents(self, query: str):

        index_data = cache.get(CACHE_KEY)

        # If index is not ready yet
        if not index_data:
            return []

        vectorizer = index_data["vectorizer"]
        doc_vectors = index_data["doc_vectors"]
        doc_ids = index_data["doc_ids"]

        # Fetch fresh ORM objects
        documents = Document.objects.in_bulk(doc_ids)

        question_vector = vectorizer.transform([query]).toarray()[0]

        dot_products = np.dot(doc_vectors, question_vector)
        doc_norms = np.linalg.norm(doc_vectors, axis=1)
        question_norm = np.linalg.norm(question_vector)

        similarities = dot_products / (doc_norms * question_norm + 1e-10)

        valid_indices = np.where(
            similarities >= self.similarity_threshold
        )[0]

        sorted_indices = valid_indices[
            np.argsort(similarities[valid_indices])[::-1]
        ]

        results = []

        for idx in sorted_indices:
            doc_id = doc_ids[idx]
            doc = documents.get(doc_id)

            if not doc:
                continue

            results.append(
                LCDocument(
                    page_content=doc.content,
                    metadata={
                        "id": doc.id,
                        "title": doc.title
                    }
                )
            )

        return results
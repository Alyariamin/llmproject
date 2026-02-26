from .models import Document, Survey
from .serializers import DocumentSerializer
from .retriever import TFIDFRetriever
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from django.conf import settings

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
class LangChainQAAPIView(APIView):

    def post(self, request):
        question = request.data.get("question")

        if not question:
            return Response(
                {"error": "Question is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        retriever = TFIDFRetriever()

        llm = ChatOpenAI(
            model="liquid/lfm-2.5-1.2b-thinking:free",
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.2,
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        result = qa_chain.invoke({"query": question})
        doc_ids = [doc.metadata["id"] for doc in result["source_documents"]]
        matched_documents = Document.objects.filter(id__in=doc_ids)
        survey = Survey.objects.create(question=question,answer=result["result"])
        survey.documents.set(matched_documents)
        return Response({
            "question": question,
            "answer": result["result"],
            "sources": [
                doc.metadata["title"]
                for doc in result["source_documents"]
            ]
        })
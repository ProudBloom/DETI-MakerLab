from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from detimakerlab.technician_api.models import Project
from detimakerlab.wiki.models import Article
from detimakerlab.wiki.serializer import ArticleSerializer

import logging
logger = logging.getLogger(__name__)


class ListAllArticles(generics.ListAPIView):
    """
        GET method to list all articles in dB
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class DependenciesView(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response('Article not found', status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        a = self.request.data['project']
        print(a)
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response('{Error: serializer invalid}', status=HTTP_404_NOT_FOUND)
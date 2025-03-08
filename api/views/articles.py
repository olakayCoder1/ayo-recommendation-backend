from rest_framework import generics

from api.serializers.articles import ArticleSerializer
from account.models import Article
from helper.utils.response.response_format import success_response




class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer


    def get_queryset(self, size=None):
        queryset = Article.objects.all()

        if size:
            return queryset.order_by('?')[:int(size)]  
        return queryset 

    def get(self, request, *args, **kwargs):
        size = request.GET.get("page_size")
        return success_response(
            data=self.serializer_class(self.get_queryset(size=size),many=True).data
        )


    

class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'


    def get(self, request, *args, **kwargs):
        return success_response(
            data=self.serializer_class(self.get_object()).data
        )


    
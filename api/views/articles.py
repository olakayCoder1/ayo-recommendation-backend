import random
from django.http import Http404
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from api.serializers.articles import ArticleSerializer
from account.models import Article, ArticleLike,ArticleBookmark
from helper.utils.response.response_format import success_response, paginate_success_response, bad_request_response




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


    



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    

        
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(channel__name__icontains=search_query)
            ).distinct()
        
        channel = self.request.query_params.get('channel', None)
        if channel:
            queryset = queryset.filter(channel__slug=channel)
        
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name=tag)
            
        return queryset
    
    # def create(self, request, *args, **kwargs):
    #     # Handle the case when tags come as a string instead of a list
    #     if 'tags' in request.data and isinstance(request.data['tags'], str):
    #         request.data['tags_list'] = [tag.strip() for tag in request.data['tags'].split(',') if tag.strip()]
            
    #     return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True,context={'request': request})
        return paginate_success_response(
            request,
            serializer.data,
            page_size=int(request.GET.get("page_size",2))
        )
    
    # def destroy(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     obj.delete()
    #     return success_response(
    #         message="Article deleted successfully"
    #     )


    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        article = self.get_object()
        user = request.user

        # Check if the user already liked the video
        if ArticleLike.objects.filter(article=article, user=user).exists():
            return bad_request_response(
                message='You have already liked this article.'
            )

        # Create the like
        ArticleLike.objects.create(article=article, user=user)

        return success_response(
            message='Article liked successfully'
        )



    @action(detail=False, methods=['get'], url_path='recommendation')
    def recommendation(self, request):
        articles = Article.objects.all()

        if articles.count() < 3:
            random_articles = articles
        else:
            random_articles = random.sample(list(articles), 5)  

        serializer = self.get_serializer(random_articles, many=True)
        return success_response(serializer.data)
    


    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        article = self.get_object()
        user = request.user

        # Check if the user already bookmarked the article
        if ArticleBookmark.objects.filter(article=article, user=user).exists():
            return bad_request_response(
                message='You have already bookmarked this article.'
            )

        # Create the bookmark
        ArticleBookmark.objects.create(article=article, user=user)

        return success_response(
            message='Article bookmarked successfully'
        )

    @action(detail=True, methods=['delete'])
    def unbookmark(self, request, pk=None):
        article = self.get_object()
        user = request.user

        # Try to find and delete the bookmark
        try:
            bookmark = ArticleBookmark.objects.get(article=article, user=user)
            bookmark.delete()
            return success_response(
                message='Article bookmark removed successfully'
            )
        except ArticleBookmark.DoesNotExist:
            return bad_request_response(
                message='You have not bookmarked this article.'
            )

    @action(detail=False, methods=['get'])
    def bookmarked(self, request):
        user = request.user
        bookmarked_articles = Article.objects.filter(bookmarks__user=user)
        
        serializer = self.get_serializer(bookmarked_articles, many=True, context={'request': request})
        return paginate_success_response(
            request,
            serializer.data,
            page_size=int(request.GET.get("page_size",2000))
        )
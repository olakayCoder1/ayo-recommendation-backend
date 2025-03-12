# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q

from api.models.other import Category, Tag
from api.models.videos import Video
from api.serializers.videos import CategorySerializer, TagSerializer, VideoSerializer
from helper.utils.response.response_format import success_response, paginate_success_response

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    parser_classes = (MultiPartParser, FormParser)
    
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
    
    def create(self, request, *args, **kwargs):
        # Handle the case when tags come as a string instead of a list
        if 'tags' in request.data and isinstance(request.data['tags'], str):
            request.data['tags_list'] = [tag.strip() for tag in request.data['tags'].split(',') if tag.strip()]
            
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return paginate_success_response(
            request,
            serializer.data,
            page_size=int(request.GET.get("page_size",20))
        )
    
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return success_response(
            message="Video deleted successfully"
        )

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
            
        return queryset

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
            
        return queryset
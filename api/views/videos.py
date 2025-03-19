# views.py
import random
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from django.db.models import Q

from api.models.other import Category, Tag
from api.models.videos import Like, Rating, Video
from api.serializers.videos import CategorySerializer, TagSerializer, VideoSerializer
from helper.utils.response.response_format import success_response, paginate_success_response, bad_request_response

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('-created_at')
    serializer_class = VideoSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    

    def get_object(self):
        video_id = self.kwargs['pk']
        print(f"Fetching video with ID: {video_id}")
        try:
            return Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise Http404
        
        
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
        serializer = self.get_serializer(queryset, many=True,context={'request': request})
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


    @action(detail=False, methods=['get'], url_path='recommendation')
    def recommendation(self, request):
        articles = Video.objects.all()

        if articles.count() < 3:
            random_articles = articles
        else:
            random_articles = random.sample(list(articles), 3)  

        serializer = self.get_serializer(random_articles, many=True)
        return success_response(serializer.data)
    
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        video = self.get_object()
        user = request.user
        rating_value = request.data.get('rating')

        if rating_value not in [1, 2, 3, 4, 5]:
            return bad_request_response(
                message="Rating must be between 1 and 5."
            )

        # Update or create the rating
        rating, created = Rating.objects.update_or_create(
            video=video, user=user,
            defaults={'rating': rating_value}
        )

        return success_response(
            message='Rating updated successfully' if not created else 'Rating added successfully'
        )
    

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        video = self.get_object()
        user = request.user

        # Check if the user already liked the video
        if Like.objects.filter(video=video, user=user).exists():
            return bad_request_response(
                message='You have already liked this video.'
            )

        # Create the like
        Like.objects.create(video=video, user=user)

        return success_response(
            message='Video liked successfully'
        )



    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        video = self.get_object()
        
        limit = request.query_params.get('limit', 6)
        
        try:
            limit = int(limit)
        except ValueError:
            limit = 6  

        related_videos = Video.objects.filter(tags__in=video.tags.all()).exclude(id=video.id).distinct()[:limit]

        # Serialize the related videos
        serializer = self.get_serializer(related_videos, many=True, context={'request': request})
        
        return success_response(data=serializer.data)


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
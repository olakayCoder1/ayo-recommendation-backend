# serializers.py
from rest_framework import serializers

from api.models.other import Category, Tag
from api.models.videos import Video

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


# class VideoSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     tags = TagSerializer(many=True, read_only=True)
#     tags_list = serializers.ListField(
#         child=serializers.CharField(max_length=50),
#         write_only=True,
#         required=False
#     )
#     category_name = serializers.CharField(write_only=True)
    
#     class Meta:
#         model = Video
#         fields = [
#             'id', 'title', 'slug', 'description', 'category', 
#             'tags', 'tags_list', 'video_file', 'thumbnail', 
#             'created_at', 'views', 'category_name'
#         ]
#         read_only_fields = ['id', 'slug', 'created_at', 'views', 'category']
    
#     def create(self, validated_data):
#         tags_list = validated_data.pop('tags_list', [])
#         category_name = validated_data.pop('category_name')
        
#         # Get or create channel
#         channel, _ = Category.objects.get_or_create(name=category_name)
#         validated_data['channel'] = channel
        
#         # Create video
#         video = Video.objects.create(**validated_data)
        
#         # Add tags
#         for tag_name in tags_list:
#             tag, _ = Tag.objects.get_or_create(name=tag_name)
#             video.tags.add(tag)
        
#         return video



class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    # tags_ids = serializers.ListField(
    #     child=serializers.CharField(),
    #     write_only=True,
    #     required=False
    # )
    tags_ids = serializers.CharField(write_only=True)
    category_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'slug', 'description', 'category', 
            'tags', 'tags_ids', 'video_file', 'thumbnail', 
            'created_at', 'views', 'category_id'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'views', 'category']
    
    def create(self, validated_data):
        tags_ids = validated_data.pop('tags_ids', '')
        print(tags_ids)
        category_id = validated_data.pop('category_id')
        
        # Get category by ID
        try:
            category = Category.objects.get(id=category_id)
            validated_data['category'] = category
        except Category.DoesNotExist:
            raise serializers.ValidationError({"category_id": "Category not found"})
        
        # Create video
        video = Video.objects.create(**validated_data)
        
        # Add tags by ID
        for tag_id in tags_ids.split(","):
            try:
                tag = Tag.objects.get(id=tag_id)
                video.tags.add(tag)
            except Tag.DoesNotExist:
                continue  # Skip invalid tag IDs
        
        return video
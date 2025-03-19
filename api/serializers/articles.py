from rest_framework import serializers

from account.models import Article, ArticleLike




class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = [
            'id','title','authors',"publish_date",
            'source_url','text','keywords','top_image',
            "meta_description","summary",'created_at','likes_count',
            "has_liked"
        ]

    def get_likes_count(self, obj:Article):
        return obj.get_likes_count()

    def get_has_liked(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return ArticleLike.objects.filter(article=obj, user=user).exists()
        return False
    
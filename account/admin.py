from django.contrib import admin
from account.models import User, Article, ArticleBookmark, ArticleLike
# Register your models here.

admin.site.register(User)
admin.site.register(Article)
admin.site.register(ArticleBookmark)
admin.site.register(ArticleLike)

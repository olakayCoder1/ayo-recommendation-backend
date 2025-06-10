from django.contrib import admin
from api.models.other import Tag, Category
from api.models.quiz import Question,Quiz,QuizAttempt
from api.models.videos import Video, Rating, Like
# Register your models here.


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizAttempt)
admin.site.register(Video)
admin.site.register(Rating)
admin.site.register(Like)
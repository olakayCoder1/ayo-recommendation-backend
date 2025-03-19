from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from account.views.auth import AccountVerifyCodeView, LoginTokenObtainPairView, RegisterUserView
from api.views.articles import ArticleListView,ArticleDetailView, ArticleViewSet
from api.views.quiz import QuizViewSet
from api.views.students import StudentViewSet
from api.views.videos import ChannelViewSet, TagViewSet, VideoViewSet
from helper.utils.scrape import GoogleDataHandler



router = DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'categories', ChannelViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'students', StudentViewSet)


urlpatterns = [
    path('account/', include('account.urls')),
    path('auth/login', LoginTokenObtainPairView.as_view()),
    path('auth/register', RegisterUserView.as_view()),
    path('auth/set-password', AccountVerifyCodeView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('articles', ArticleListView.as_view(), name='token_refresh'),
    path('article/<uuid:id>', ArticleDetailView.as_view(), name='token_refresh'),
    path('article/<uuid:id>/', ArticleDetailView.as_view(), name='token_refresh'),
    path('article/<uuid:id>/', ArticleDetailView.as_view(), name='token_refresh'),

    path('admin/', include(router.urls)),
]

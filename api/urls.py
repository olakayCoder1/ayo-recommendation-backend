from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import include, path
from account.views.auth import AccountVerifyCodeView, LoginTokenObtainPairView, RegisterUserView
from api.views.articles import ArticleListView,ArticleDetailView
from helper.utils.scrape import GoogleDataHandler


urlpatterns = [
    path('account/', include('account.urls')),
    path('auth/login', LoginTokenObtainPairView.as_view()),
    path('auth/register', RegisterUserView.as_view()),
    path('auth/set-password', AccountVerifyCodeView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('articles', ArticleListView.as_view(), name='token_refresh'),
    path('article/<uuid:id>', ArticleDetailView.as_view(), name='token_refresh'),
    path('article/<uuid:id>/', ArticleDetailView.as_view(), name='token_refresh'),
]

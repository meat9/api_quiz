from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register('quizs', views.Quiz_View_Set)
router.register('quizs/(?P<id>\d+)/questions',views.Question_View_Set,basename='questions')
router.register('quizs/(?P<id>\d+)/questions/(?P<question_pk>\d+)/choices',views.Choice_View_Set,basename='choices')
router.register('active_quizs', views.Active_Quiz_List)
router.register('quizs/(?P<id>\d+)/questions/(?P<question_pk>\d+)/answers',views.Answer_Create_View_Set,basename='answers')
router.register('my_quizs',views.UserId_Quiz_List_View_Set,basename='list_userid_quizs')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

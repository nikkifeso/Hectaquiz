from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import QuizList, DeleteQuiz

urlpatterns = [
    path('quiz-list/', QuizList.as_view(), name='quiz_list'),
    path('delete-quiz/', DeleteQuiz.as_view(), name='delete_quiz'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
from django.urls import path, re_path
from .views import(
     QuizDetails, QuizList, RegistrationView, LoginView, 
     UserRetrieveUpdateView, UserQuizList, SaveUserAnswers,
     SubmitQuiz, FacebookLogin, GoogleLogin
)

urlpatterns = [
    path('my-quizzes/', UserQuizList.as_view(), name='my_quiz_list'),
    path('save-answers/', SaveUserAnswers.as_view(), name='save_answers'),
    re_path(r"quiz/(?P<slug>[\w\-]+)/submit/$", SubmitQuiz.as_view(), name='submit_quiz'),
    path('quizzes/', QuizList.as_view(), name='quiz_list'),
    re_path(r"quiz/(?P<slug>[\w\-]+)/$", QuizDetails.as_view(), name='quiz_details'),
    path('users/register/', RegistrationView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('user/', UserRetrieveUpdateView.as_view(), name='user'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
]
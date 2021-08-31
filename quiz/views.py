from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Quiz, QuizTaker, Question, UsersAnswer, User, Answer
from .serializers import (
    QuizSerializer, QuizDetailsSerializer, RegistrationSerializer,
    LoginSerializer, UserSerializer, UsersAnswerSerializer,
    ResultsSerializer, UserQuizSerializer, ResultsSerializer
)

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

import datetime


class UserQuizList(generics.ListAPIView):
    serializer_class = UserQuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       queryset = Quiz.objects.filter(quiztaker__user=self.request.user)
       return queryset


class QuizList(generics.ListAPIView):
    """Returns All Quizzez Available"""
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filters rolled-outed quizzes"""
        queryset = Quiz.objects.filter(roll_out=True).exclude(quiztaker__user=self.request.user)
        return queryset


class QuizDetails(generics.RetrieveAPIView):
    """Returns details for specified quiz"""
    serializer_class = QuizDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        slug = self.kwargs['slug']
        quiz = get_object_or_404(Quiz, slug=slug)
        last_question = None
        obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
        for question in Question.objects.filter(quiz=quiz):
                UsersAnswer.objects.create(quiz_taker=obj, question=question)
        last_question = UsersAnswer.objects.filter(quiz_taker=obj, answer__isnull=False)
        if last_question.count()> 0:
            last_question= last_question.last().question.id
        last_question = None
        return Response({'quiz': self.get_serializer(quiz, context={'request': self.request}).data,'last_question_id': last_question})


class SaveUserAnswers(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersAnswerSerializer

    def patch(self, request):
        quiztaker_id = request.data['quiztaker']
        question_id = request.data['question']
        answer_id = request.data['answer']

        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        if quiztaker.completed:
            response = {
            'message': 'Quiz completed! You cannot answer any more questions'}
            return Response(response, status= status.HTTP_412_PRECONDITION_FAILED)

        obj = get_object_or_404(UsersAnswer, quiz_taker=quiztaker, question=question)
        obj.answer = answer
        obj.save()
        
        return Response(self.get_serializer(obj).data)

class SubmitQuiz(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultsSerializer

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        quiztaker_id = request.data['quiztaker']
        question_id = request.data['question']
        answer_id = request.data['answer']

        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
        question = get_object_or_404(Question, id=question_id)

        if quiztaker.completed:
            response = {
            'message': 'Submit successful! You cannot submit again'}
            return Response(response, status= status.HTTP_412_PRECONDITION_FAILED)
        if answer_id:
            answer = get_object_or_404(Answer, id=answer_id)
            obj = get_object_or_404(UsersAnswer, quiz_taker=quiztaker, question=question)
            obj.answer = answer
            obj.save()

        quiztaker.completed = True
        correct_answers = 0
        for users_answer in UsersAnswer.objects.filter(quiz_taker=quiztaker):
            answer = Answer.objects.get(question=users_answer.question, is_correct=True)
            if users_answer.answer == answer:
                correct_answers+= 1
        quiztaker.score = int(correct_answers/quiztaker.quiz.question_set.count())*100
        # quiztaker.date_completed = datetime.datetime.now()
        quiztaker.save()

        return Response(self.get_serializer(quiztaker).data)


class RegistrationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = RegistrationSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        name = user.get('name', '')
        email = user.get('email','')
        username =user.get('username','')
        password= user.get('password', '')

        users = get_user_model().objects.create(
            name=name,
            email=email,
            username = username,
            password = password,
        )
        users.set_password(password)
        users.save()

        return Response({'data':serializer.data, 'status':status.HTTP_201_CREATED})


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'message': 'User logged in  successfully',
          
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    

    def get(self,request):
        serializer_class = UserSerializer
        try:
            user = request.user
            serializer = self.serializer_class(data=user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile retrieved successfully',
                'data': [{
                    'name': user.name,
                    'email': user.email,
                    'username': user.username,
                    }]
                }
                
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

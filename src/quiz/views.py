from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Quiz, QuizTaker, Question, UsersAnswer, User
from .serializers import QuizSerializer, QuizDetailsSerializer


class QuizList(generics.ListAPIView):
    """Returns All Quizzez Available"""
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filters rolled-outed quizzes"""
        return Quiz.objects.filter(roll_out=True)

class QuizDetails(generics.RetrieveAPIView):
    """Returns details for specified quiz"""
    serializer_class = QuizDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        slug = self.kwargs['slug']
        quiz = get_object_or_404(Quiz, slug=slug)
        last_question = None
        obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
        if created:
            for question in Question.object.filter(quiz=quiz):
                UsersAnswer.objects.create(quiz_taker=obj, question=question)
        else:
            last_question = UsersAnswer.object.filter(quiz_taker=obj, not_answered=False)
            if last_question.count()> 0:
                last_question= last_question.last().question.id
            last_question = None
        return Response({'quiz': self.get_serializer(quiz, context={'request': self.request}).data,'last_question': last_question})
            

class DeleteQuiz(generics.DestroyAPIView):
    """Deletes the particuler quiz"""
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, *args, **kwargs):
        slug = self.kwargs['slug']
        queryset = Quiz.objects.filter(quiz=self.request.user, slug=slug)
        return queryset
    
    def destroy(self):
        instance = self.get_object()
        self.perform_destroy(instance)


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
           user = serializer.save()
           return Response({
               'user': UserSerializer(user).data,
               'token':
           })
    

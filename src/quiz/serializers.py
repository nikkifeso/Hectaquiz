from rest_framework import serializers
from django.conf import settings
from .models import Quiz, Question, Answer, QuizTaker, UsersAnswer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email_valid = 'email' in data and data['email']
        confirm_password = 'confirm_password' in data and data['confirm_password'].strip()
        password_match = data['password'].strip() == data['confirm_password'].strip()
        validate_password(password=data['password'].strip())

        errors = {}
        if not confirm_password:
            errors['confirm_password'] = ['This field cannot be empty']

        if not password_match:
            errors['password_match'] = ['Passwords do not match']

        if not email_valid:
            errors['email'] = ['Invalid email']

        if len(errors):
            raise serializers.ValidationError(errors)

        return data

class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id','name','description','slug','image', 'questions_count']
    def get_questions_count(self, obj):
        return obj.question_set.all().count()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','quiz','label']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'label']


class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAnswer
        fields = '__all__'


class QuizTakerSerializer(serializers.ModelSerializer):
    users_answer_set = UsersAnswerSerializer(many=True)
    class Meta:
        model = QuizTaker
        fields = '__all__'


class QuizDetailsSerializer(serializers.ModelSerializer):
    quiztakers_set = serializers.SerializerMethodField()
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_quiztaker_set(self, obj):
        try:
            quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            serializer = QuizTakerSerializer(quiz_taker)
            return serializer.data
        except QuizTaker.DoesNotExist:
            return None
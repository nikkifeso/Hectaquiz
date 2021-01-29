from rest_framework import serializers
from django.conf import settings
from .models import Quiz, Question, Answer, QuizTaker, UsersAnswer, User
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id','name','description','slug','image', 'questions_count']
    def get_questions_count(self, obj):
        return obj.question_set.all().count()

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'label']


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = '__all__'


class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAnswer
        fields = '__all__'


class QuizTakerSerializer(serializers.ModelSerializer):
    usersanswer_set = UsersAnswerSerializer(many=True)
    class Meta:
        model = QuizTaker
        fields = '__all__'


class QuizDetailsSerializer(serializers.ModelSerializer):
    quiztaker_set = serializers.SerializerMethodField()
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

            
class ResultsSerializer(serializers.ModelSerializer):
	quiztaker_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztaker_set(self, obj):
		try:
			quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			serializer = QuizTakerSerializer(quiztaker)
			return serializer.data

		except QuizTaker.DoesNotExist:
			return None 

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length = 8,
        max_length = 128,
        write_only = True
    )
    token = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password', 'token']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=email, password=password)

        if email is None or password is None:
            raise serializers.ValidationError("Email Address and Password are required to login")
        if  not user:
            raise serializers.ValidationError("User with this email and password combination was not found")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            'email':user.email,
            'token': jwt_token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length = 8,
        max_length = 128,
        write_only = True
    )
    class Meta:
        model = User
        fields = ['email', 'username', 'name']



class UserQuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields =['id', 'name', 'description', 'slug', 'image', 'questions_count', 'completed', 'score', 'progress']
        read_only_fields = ['questions_count', 'completed', 'score', 'progress']

    def get_questions_count(self, obj):
        return obj.question_set.all().count()


    def get_completed(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            return quiztaker.completed
        except QuizTaker.DoesNotExist:
            return None


    def get_score(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed:
                return quiztaker.score
        except QuizTaker.DoesNotExist:
            return None


    def get_progress(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if not quiztaker.completed:
                answered = UsersAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
                total_questions = obj.question_set.all().count()
                return int(answered/total_questions)*100
            return None
        except QuizTaker.DoesNotExist:
            return None

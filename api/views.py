from rest_framework import viewsets, mixins, permissions
from rest_framework.generics import get_object_or_404
from api.models import Quiz, Question, Answer, Choice
from api.serializers import (
    Quiz_Serializer, Question_Serializer, Answer_Serializer,
    User_Quiz_Serializer, Answer_One_Text_Serializer,
    Answer_One_Choice_Serializer, Answer_Multiple_Choice_Serializer,
    Choice_Serializer,
)
from datetime import datetime
from django.db.models import Q


class Quiz_View_Set(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = Quiz_Serializer
    permission_classes = (permissions.IsAdminUser,)


class Question_View_Set(viewsets.ModelViewSet):
    serializer_class = Question_Serializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['id'])
        serializer.save(quiz=quiz)

    def get_queryset(self):
        quiz = get_object_or_404(Quiz, id=self.kwargs['id'])
        return quiz.questions.all()


class Choice_View_Set(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = Choice_Serializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        question = get_object_or_404(Question,pk=self.kwargs['question_pk'],quiz__id=self.kwargs['id'],)
        serializer.save(question=question)

    def get_queryset(self):
        question = get_object_or_404(Question, id=self.kwargs['question_pk'])
        return question.choices.all()


class Active_Quiz_List(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Quiz.objects.filter(end_date__gte=datetime.today())
    serializer_class = Quiz_Serializer
    permission_classes = (permissions.AllowAny,)


class Answer_Create_View_Set(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = Answer_Serializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        question = get_object_or_404(Question,pk=self.kwargs['question_pk'],quiz__id=self.kwargs['id'],)
        serializer.save(author=self.request.user, question=question)

    def get_serializer_class(self):
        question = get_object_or_404(Question,pk=self.kwargs['question_pk'],quiz__id=self.kwargs['id'],)
        if question.type_question == 'text_field':
            return Answer_One_Text_Serializer
        elif question.type_question == 'radio':
            return Answer_One_Choice_Serializer
        else:
            return Answer_Multiple_Choice_Serializer


class UserId_Quiz_List_View_Set(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = User_Quiz_Serializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Quiz.objects.exclude(~Q(questions__answers__author__id=user_id))
        return queryset








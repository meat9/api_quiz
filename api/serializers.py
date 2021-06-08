from rest_framework import serializers
from api.models import Quiz, Question, Answer, Choice
from django.db.models import Q


#Сериалайзер опросов
class Quiz_Serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Quiz


#Сериалайзер вариантов ответов
class Choice_Serializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Choice


#Сериалайзер вопросов
class Question_Serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Question


#Сериалайзер ответов пользователей
class Answer_Serializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Answer


#Сериалайзер вопросов с ответами юзеров
class Question_List_Serializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        fields = ['text', 'answers']
        model = Question

    def get_answers(self, question):
        # author_id = self.context.get('request').parser_context['kwargs']['id']
        author_id = self.context.get('request').user.id
        answers = Answer.objects.filter(Q(question=question) & Q(author__id=author_id))
        serializer = Answer_Serializer(instance=answers, many=True)
        return serializer.data


#Сериалайзер опросов с вопросами и ответами юзеров
class User_Quiz_Serializer(serializers.ModelSerializer):
    questions = Question_List_Serializer(read_only=True, many=True)

    class Meta:
        fields = '__all__'
        model = Quiz


#Сериалайзер ответа своим текстом
class Answer_One_Text_Serializer(serializers.ModelSerializer):
    class Meta:
        fields = ['self_text']
        model = Answer


class User_Filtered_Field(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        question_id = self.context.get('request').parser_context['kwargs']['question_pk']
        request = self.context.get('request', None)
        queryset = super(User_Filtered_Field,self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)


#Сериалайзер ответа выбором одного варианта
class Answer_One_Choice_Serializer(serializers.ModelSerializer):
    one_choice = User_Filtered_Field(many=False,queryset=Choice.objects.all())

    class Meta:
        fields = ['one_choice']
        model = Answer


#Сериалайзер ответа выбором нескольких вариантов
class Answer_Multiple_Choice_Serializer(serializers.ModelSerializer):
    many_choice = User_Filtered_Field(many=True,queryset=Choice.objects.all())

    class Meta:
        fields = ['many_choice']
        model = Answer

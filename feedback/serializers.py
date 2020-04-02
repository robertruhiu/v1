from rest_framework import serializers

from feedback.models import RecruiterFeedback, SurveyQuestion, SurveyAnswer, Choice
from frontend.serializers import ProfileSerializer
from marketplace.serializers import JobApplicationsRequestSerializer, JobRequestSerializer, \
    MyapplicantsRequestSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice', 'position']


class SurveyQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = ['type', 'question', 'choices','id']


class RecruiterFeedbackSerializer(serializers.ModelSerializer):
    # customer = ProfileSerializer()
    # job = JobRequestSerializer()
    survey_questions = SurveyQuestionSerializer(many=True, read_only=True)
    developers = JobApplicationsRequestSerializer(many=True, read_only=True)

    class Meta:
        model = RecruiterFeedback
        fields = ('slug','survey_questions', 'developers', )
        # survey_questions, 'developers',)


class SurveyAnswerSerializer(serializers.ModelSerializer):
    feedback_model = RecruiterFeedbackSerializer
    question = SurveyQuestionSerializer
    developer = ProfileSerializer

    class Meta:
        model = SurveyAnswer
        fields = '__all__'

from django.db import models

# Create your models here.
from accounts.models import Profile
from marketplace.models import Job, JobApplication


class RecruiterFeedback(models.Model):
    customer = models.OneToOneField(Profile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    satisfied = models.BooleanField(default=False)

    @property
    def developers(self):
        return JobApplication.objects.filter(recruiter=self.customer, job=self.job, stage='active')

    @property
    def survey_questions(self):
        return SurveyQuestion.objects.all()

    def __str__(self):
        return f'{self.customer.full_name} - {self.job.title} feedback'


class SurveyQuestion(models.Model):
    TYPE_CHOICES = (
        ('codeln_survey', 'CODELN SURVEY'),
        ('dev_survey', 'DEV SURVEY'),
        ('job_survey', 'JOB SURVEY'),
    )
    type = models.CharField(max_length=140, default='codeln_survey', choices=TYPE_CHOICES)
    question = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.type} - {self.question}'


class Choice(models.Model):
    question = models.ForeignKey("SurveyQuestion", on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField("Choice", max_length=50)
    position = models.IntegerField("position")

    class Meta:
        unique_together = [
            # no duplicated choice per question
            ("question", "choice"),
            # no duplicated position per question
            ("question", "position")
        ]
        ordering = ("position",)

    def __str__(self):
        return f'{self.question} - {self.choice}'


class SurveyAnswer(models.Model):
    feedback_model = models.ForeignKey(RecruiterFeedback, on_delete=models.CASCADE)
    question = models.ForeignKey("SurveyQuestion", on_delete=models.CASCADE, related_name="answer")
    text = models.CharField(max_length=255)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.feedback_model.customer} - {self.question} - {self.text}'

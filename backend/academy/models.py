from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


class ChildProfile(models.Model):
 parent=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='children')
 nickname=models.CharField(max_length=40)
 age=models.PositiveSmallIntegerField(validators=[MinValueValidator(8),MaxValueValidator(14)])
 created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self):return self.nickname
class LearningPath(models.Model):
 slug=models.SlugField(unique=True)
 title=models.CharField(max_length=120)
 min_age=models.PositiveSmallIntegerField()
 max_age=models.PositiveSmallIntegerField()
 def __str__(self):return self.title
class Mission(models.Model):
 path=models.ForeignKey(LearningPath,on_delete=models.CASCADE,related_name='missions')
 slug=models.SlugField(unique=True)
 title=models.CharField(max_length=140)
 summary=models.TextField()
 objectives=models.JSONField(default=list)
 order=models.PositiveIntegerField(default=1)
 duration_minutes=models.PositiveIntegerField(default=18)
 is_published=models.BooleanField(default=False)
 class Meta:ordering=['order']
 def __str__(self):return self.title
class Activity(models.Model):
 mission=models.ForeignKey(Mission,on_delete=models.CASCADE,related_name='activities')
 order=models.PositiveIntegerField()
 title=models.CharField(max_length=140)
 kind=models.CharField(max_length=20,choices=[('story','Story'),('choice','Choice'),('reflection','Reflection')])
 content=models.JSONField(default=dict)
 class Meta:ordering=['order'];unique_together=[('mission','order')]
class QuizQuestion(models.Model):
 mission=models.ForeignKey(Mission,on_delete=models.CASCADE,related_name='questions')
 order=models.PositiveIntegerField()
 prompt=models.CharField(max_length=350)
 options=models.JSONField(default=list)
 correct_index=models.PositiveSmallIntegerField()
 explanation=models.TextField()
 class Meta:ordering=['order'];unique_together=[('mission','order')]
class Badge(models.Model):
 slug=models.SlugField(unique=True)
 title=models.CharField(max_length=100)
 description=models.CharField(max_length=250)
 mission=models.OneToOneField(Mission,on_delete=models.CASCADE,related_name='badge')
class MissionProgress(models.Model):
 child=models.ForeignKey(ChildProfile,on_delete=models.CASCADE,related_name='progress')
 mission=models.ForeignKey(Mission,on_delete=models.CASCADE)
 completed=models.BooleanField(default=False)
 best_score=models.PositiveSmallIntegerField(default=0)
 xp=models.PositiveIntegerField(default=0)
 completed_at=models.DateTimeField(null=True,blank=True)
 class Meta:unique_together=[('child','mission')]
class QuizAttempt(models.Model):
 child=models.ForeignKey(ChildProfile,on_delete=models.CASCADE,related_name='attempts')
 mission=models.ForeignKey(Mission,on_delete=models.CASCADE)
 answers=models.JSONField(default=dict)
 score=models.PositiveSmallIntegerField()
 total=models.PositiveSmallIntegerField()
 created_at=models.DateTimeField(auto_now_add=True)
class ChildBadge(models.Model):
 child=models.ForeignKey(ChildProfile,on_delete=models.CASCADE,related_name='badges')
 badge=models.ForeignKey(Badge,on_delete=models.CASCADE)
 awarded_at=models.DateTimeField(auto_now_add=True)
 class Meta:unique_together=[('child','badge')]

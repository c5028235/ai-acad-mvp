from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import ChildProfile,Mission,Activity,QuizQuestion,MissionProgress,ChildBadge
class RegisterSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True,validators=[validate_password])
 class Meta:model=User;fields=['id','username','email','password']
 def create(self,data):return User.objects.create_user(**data)
class ChildSerializer(serializers.ModelSerializer):
 class Meta:model=ChildProfile;fields=['id','nickname','age','created_at'];read_only_fields=['id','created_at']
class ActivitySerializer(serializers.ModelSerializer):
 class Meta:model=Activity;fields=['id','order','title','kind','content']
class QuestionSerializer(serializers.ModelSerializer):
 class Meta:model=QuizQuestion;fields=['id','order','prompt','options']
class MissionSerializer(serializers.ModelSerializer):
 activities=ActivitySerializer(many=True,read_only=True)
 questions=QuestionSerializer(many=True,read_only=True)
 path=serializers.CharField(source='path.title',read_only=True)
 class Meta:model=Mission;fields=['id','slug','title','summary','objectives','duration_minutes','path','activities','questions']
class ProgressSerializer(serializers.ModelSerializer):
 mission_title=serializers.CharField(source='mission.title',read_only=True)
 class Meta:model=MissionProgress;fields=['mission_title','completed','best_score','xp','completed_at']
class ChildBadgeSerializer(serializers.ModelSerializer):
 title=serializers.CharField(source='badge.title',read_only=True)
 class Meta:model=ChildBadge;fields=['title','awarded_at']

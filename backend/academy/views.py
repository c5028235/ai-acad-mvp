from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ChildProfile,Mission,MissionProgress,QuizAttempt,ChildBadge
from .serializers import RegisterSerializer,ChildSerializer,MissionSerializer,ProgressSerializer,ChildBadgeSerializer
class RegisterView(generics.CreateAPIView):
 serializer_class=RegisterSerializer;permission_classes=[AllowAny]
class ChildListCreate(generics.ListCreateAPIView):
 serializer_class=ChildSerializer
 def get_queryset(self):return ChildProfile.objects.filter(parent=self.request.user).order_by('id')
 def perform_create(self,serializer):serializer.save(parent=self.request.user)
class MissionDetail(generics.RetrieveAPIView):
 serializer_class=MissionSerializer;lookup_field='slug'
 def get_queryset(self):return Mission.objects.filter(is_published=True).prefetch_related('activities','questions')
class ChildProgress(APIView):
 def get(self,request,child_id):
  child=get_object_or_404(ChildProfile,id=child_id,parent=request.user)
  progress=MissionProgress.objects.filter(child=child).select_related('mission')
  badges=ChildBadge.objects.filter(child=child).select_related('badge')
  return Response({'child':ChildSerializer(child).data,'progress':ProgressSerializer(progress,many=True).data,'badges':ChildBadgeSerializer(badges,many=True).data})
class SubmitQuiz(APIView):
 def post(self,request,child_id,slug):
  child=get_object_or_404(ChildProfile,id=child_id,parent=request.user)
  mission=get_object_or_404(Mission,slug=slug,is_published=True)
  if not mission.path.min_age<=child.age<=mission.path.max_age:
   return Response({'detail':'Mission is not for this age group.'},status=403)
  questions=list(mission.questions.all())
  answers=request.data.get('answers')
  if not isinstance(answers,dict) or not questions:
   return Response({'detail':'Answers must be an object.'},status=400)
  expected={str(q.id) for q in questions}
  if set(answers)!=expected or any(type(answers[str(q.id)]) is not int or not 0<=answers[str(q.id)]<len(q.options) for q in questions):
   return Response({'detail':'Provide one valid answer index for each question.'},status=400)
  score=sum(answers[str(q.id)]==q.correct_index for q in questions)
  passed=score*5>=len(questions)*4
  feedback=[{'id':q.id,'correct_index':q.correct_index,'explanation':q.explanation} for q in questions]
  with transaction.atomic():
   QuizAttempt.objects.create(child=child,mission=mission,answers=answers,score=score,total=len(questions))
   progress,_=MissionProgress.objects.select_for_update().get_or_create(child=child,mission=mission)
   progress.best_score=max(progress.best_score,score)
   if passed:
    progress.completed=True;progress.xp=max(progress.xp,100)
    if not progress.completed_at:progress.completed_at=timezone.now()
    if hasattr(mission,'badge'):ChildBadge.objects.get_or_create(child=child,badge=mission.badge)
   progress.save()
  return Response({'score':score,'total':len(questions),'passed':passed,'xp':progress.xp,'feedback':feedback})
